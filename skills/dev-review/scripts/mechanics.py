"""Small process, file and Git evidence primitives. No action selection."""
import hashlib
import json
import math
import os
from pathlib import Path
import selectors
import signal
import stat
import subprocess
import sys
import time

from journal import atomic_json


def load(path):
    return json.loads(Path(path).read_text())


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def contained(root, path):
    root = Path(root).resolve(strict=True)
    path = Path(path)
    path = (root / path).resolve(strict=True) if not path.is_absolute() else path.resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('artifact must be an existing file under allowed root')
    return path


def stop(process):
    """Stop the dedicated process group, including children holding output pipes."""
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def capture(command, cwd, directory, timeout, stdin=None, terminal=True, on_stdout=None):
    """Persist actual stdout/stderr bytes, PID and exit even on timeout; no shell."""
    if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('timeout must be positive')
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    started = time.time()
    if not isinstance(command, list) or not command or not all(isinstance(s, str) and s for s in command):
        raise ValueError('command must be a nonempty argv list')
    try:
        process = subprocess.Popen(command, cwd=cwd, stdin=stdin or subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   start_new_session=True)
    except OSError as error:
        result = {'command': command, 'cwd': str(cwd), 'exit_code': None, 'timed_out': False,
                  'spawn_error': str(error), 'started': started, 'finished': time.time()}
        for name in ('stdout', 'stderr'):
            with (directory / name).open('wb') as stream:
                stream.flush()
                os.fsync(stream.fileno())
        atomic_json(directory / 'exit.json', result)
        return result
    try:
        atomic_json(directory / 'process.json', {'pid': process.pid, 'owner_pid': os.getpid(),
                                               'started': started, 'command': command})
        timed_out = False
        deadline = time.monotonic() + timeout
        with selectors.DefaultSelector() as selector, (directory / 'stdout').open('wb') as out, (directory / 'stderr').open('wb') as err:
            selector.register(process.stdout, selectors.EVENT_READ, (out, sys.stdout))
            selector.register(process.stderr, selectors.EVENT_READ, (err, sys.stderr))
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    timed_out = True
                    stop(process)
                    break
                for key, _ in selector.select(min(remaining, 0.2)):
                    chunk = os.read(key.fd, 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    target, screen = key.data
                    target.write(chunk)
                    target.flush()
                    os.fsync(target.fileno())
                    if key.data[0] is out and on_stdout is not None:
                        on_stdout(chunk)
                    if terminal:
                        screen.write(chunk.decode('utf-8', errors='replace'))
                        screen.flush()
            try:
                code = process.wait(timeout=max(0.001, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                timed_out = True
                stop(process)
                code = process.returncode
            for stream in (out, err):
                stream.flush()
                os.fsync(stream.fileno())
        result = {'command': command, 'cwd': str(cwd), 'exit_code': code,
                  'timed_out': timed_out, 'started': started, 'finished': time.time()}
        atomic_json(directory / 'exit.json', result)
        return result
    finally:
        if process.poll() is None:
            stop(process)
        process.stdout.close()
        process.stderr.close()


def git(cwd, *args):
    return subprocess.run(['git', '-C', str(cwd), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30).stdout


def index_entries(cwd):
    entries = []
    for row in git(cwd, 'ls-files', '--stage', '-z').split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, oid, stage = meta.split()
            if stage != b'0':
                raise ValueError('unmerged index')
            entries.append([os.fsdecode(path), mode.decode(), oid.decode()])
    return sorted(entries)


def git_snapshot(cwd):
    """HEAD, branch, staged entries and content/mode of tracked and untracked files.

    Ignored files are excluded; separately named artifacts are hashed by verification.
    Submodules are rejected instead of reporting incomplete working-tree evidence.
    """
    cwd = Path(cwd).resolve()
    top = Path(os.fsdecode(git(cwd, 'rev-parse', '--show-toplevel')).strip()).resolve()
    if cwd != top:
        raise ValueError('cwd must be the Git repository root')
    entries = index_entries(cwd)
    if any(row[1] == '160000' for row in entries):
        raise ValueError('submodule working-tree evidence is unsupported')
    files = {}
    paths = set(git(cwd, 'ls-files', '-c', '-o', '--exclude-standard', '-z').split(b'\0')) - {b''}
    for raw in sorted(paths):
        name = os.fsdecode(raw)
        path = cwd / name
        try:
            info = path.lstat()
        except FileNotFoundError:
            files[name] = None
            continue
        mode = stat.S_IMODE(info.st_mode)
        if path.is_symlink():
            files[name] = {'mode': mode, 'link': os.readlink(path)}
        elif path.is_file():
            files[name] = {'mode': mode, 'sha256': sha256(path)}
        else:
            raise ValueError('unsupported Git working-tree entry: ' + name)
    return {'head': git(cwd, 'rev-parse', 'HEAD').decode().strip(),
            'branch': git(cwd, 'rev-parse', '--abbrev-ref', 'HEAD').decode().strip(),
            'index': entries, 'files': files}
