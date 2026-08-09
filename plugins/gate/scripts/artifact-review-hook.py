#!/usr/bin/env python3
"""artifact-review-hook.py - PreToolUse hook for Write.

Intercepts a Write to a planning artifact and shows the pending content in the
revdiff TUI before it reaches disk. Annotations come back as a blocking denial,
so the agent revises and writes again; a clean review lets the Write through.

The hook reads the event JSON on stdin and uses tool_input.file_path and
tool_input.content. Every Write outside GATED_PATTERNS passes through silently
with no decision at all, so the normal permission flow is untouched.

Exit codes:
  0 - pass through (not gated, or reviewed clean, or failed open)
  2 - blocked; stderr carries the annotations the agent must address

Requires the revdiff binary in PATH and an overlay terminal the launcher knows.
Anything missing fails open: a Write is never lost because the review could not
run.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Artifact paths that earn a review, matched against the repository-relative
# path with fnmatch. A pattern here is a deliberate choice: the file is a
# decision the user signs off on, not a byproduct. Editing this list is the
# supported way to widen or narrow the gate.
GATED_PATTERNS = (
    "docs/nxs/stories/*/brief.md",
    "docs/nxs/stories/*/root-cause.md",
    "docs/nxs/stories/*/plan.md",
    ".scratch/*/*.md",
    ".scratch/*/issues/*.md",
)

# Snapshot of the last content the user reviewed for a given target path, so a
# second round shows only what the revision changed. Keyed by a hash of the
# absolute target path, which keeps parallel sessions and unrelated artifacts
# from colliding without asking the agent to carry a marker through its output.
SNAPSHOT_PREFIX = "gate-rev-"
SUCCESS_CODES = {0, 10}


def read_event() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def passthrough(note: str = "") -> None:
    """Let the Write proceed. No JSON on stdout, so the hook contributes no
    permission decision and the normal flow decides."""
    if note:
        print(f"gate: {note}", file=sys.stderr)
    sys.exit(0)


def block(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def project_root() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())


def relative_target(file_path: str) -> str | None:
    """Repository-relative POSIX path, or None when the target sits outside the
    project. A path outside the project is never gated - the patterns describe
    this repository's layout and mean nothing elsewhere."""
    root = project_root().resolve()
    target = Path(file_path)
    if not target.is_absolute():
        target = root / target
    try:
        return target.resolve().relative_to(root).as_posix()
    except (OSError, ValueError):
        return None


def snapshot_path(file_path: str) -> Path:
    key = hashlib.sha256(str(Path(file_path).absolute()).encode()).hexdigest()[:16]
    return Path(tempfile.gettempdir()) / f"{SNAPSHOT_PREFIX}{key}.md"


def resolve_launcher(plugin_root: str) -> Path | None:
    resolver = Path(plugin_root) / "scripts" / "resolve-launcher.sh"
    if not resolver.exists():
        return None
    try:
        result = subprocess.run(
            [str(resolver), "launch-artifact-review.sh",
             os.environ.get("CLAUDE_PLUGIN_DATA", "")],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0 or not result.stdout.strip():
        if result.stderr:
            print(result.stderr.rstrip(), file=sys.stderr)
        return None
    return Path(result.stdout.strip())


def main() -> None:
    event = read_event()
    tool_input = event.get("tool_input") or {}
    file_path = tool_input.get("file_path") or ""
    content = tool_input.get("content")
    if not file_path or not isinstance(content, str):
        passthrough()

    rel = relative_target(file_path)
    if rel is None or not any(fnmatch.fnmatch(rel, p) for p in GATED_PATTERNS):
        passthrough()

    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if not plugin_root:
        passthrough("CLAUDE_PLUGIN_ROOT not set, artifact not reviewed")
    if not shutil.which("revdiff"):
        passthrough("revdiff not in PATH, artifact not reviewed")
    launcher = resolve_launcher(plugin_root)
    if launcher is None:
        passthrough("launch-artifact-review.sh not found, artifact not reviewed")

    # Baseline for the compare: the snapshot of the last round when this write
    # is a revision, otherwise the file already on disk when this write updates
    # an existing artifact. Neither means a first draft, reviewed whole.
    snapshot = snapshot_path(file_path)
    baseline: Path | None = None
    if snapshot.is_file():
        baseline = snapshot
    elif Path(file_path).is_file():
        baseline = Path(file_path)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", prefix=SNAPSHOT_PREFIX, delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(content)
        pending = Path(tmp.name)

    args = [str(launcher), str(pending), rel]
    if baseline is not None:
        args.append(str(baseline))

    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=345600)
    except (OSError, subprocess.SubprocessError) as exc:
        pending.unlink(missing_ok=True)
        passthrough(f"review launcher failed ({exc}), artifact not reviewed")

    if result.returncode not in SUCCESS_CODES:
        pending.unlink(missing_ok=True)
        detail = (result.stderr or "").strip().splitlines()
        tail = detail[-1] if detail else f"exit {result.returncode}"
        passthrough(f"review launcher failed ({tail}), artifact not reviewed")

    annotations = result.stdout.strip()
    if not annotations:
        pending.unlink(missing_ok=True)
        snapshot.unlink(missing_ok=True)
        passthrough()

    # Keep what the user just reviewed as the baseline for the next round, so
    # the revision shows up as a diff rather than as the whole file again.
    pending.replace(snapshot)
    block(
        f"The user reviewed the pending content of {rel} in revdiff and left "
        "annotations. Each one points at a line and carries their feedback.\n\n"
        f"{annotations}\n\n"
        f"Address every annotation, then write {rel} again with the full "
        "revised content. The file was NOT written - this review is the gate it "
        "passes through, and the next Write is reviewed the same way, showing "
        "only what you changed."
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\r\033[K", end="")
        sys.exit(130)
