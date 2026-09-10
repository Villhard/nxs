#!/usr/bin/env bash
# Optional PreToolUse/Bash adapter. Only plain staged git commit is supported.
set -euo pipefail
exec python3 -c '
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "deny",
        "permissionDecisionReason": reason}}))
    sys.exit(0)


try:
    payload = json.load(sys.stdin)
    command = payload["tool_input"]["command"]
    if not isinstance(command, str):
        raise ValueError("command must be a string")
except (ValueError, KeyError, TypeError) as error:
    deny(f"Invalid Bash hook payload: {error}")
try:
    lexer = shlex.shlex(command, posix=True, punctuation_chars="();<>|&\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    words = list(lexer)
except ValueError as error:
    deny(f"Cannot parse Bash hook command: {error}")
def is_commit(args):
    # Git global options precede the subcommand; later arguments are not commands.
    args = iter(args)
    for arg in args:
        if arg in ("-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env"):
            next(args, None)
        elif not arg.startswith("-"):
            return arg == "commit"
    return False


# Detect explicit git commit invocations, including wrappers and Git options.
# This is an invocation guard, not a general shell interpreter.
commit = any(Path(word).name == "git" and is_commit(words[i + 1:])
             and (i == 0 or words[i - 1] in (";", "&&", "||", "|", "(", "\n")
                  or words[0] in ("env", "command", "sudo")
                  or "=" in words[0])
             for i, word in enumerate(words))
if words and Path(words[0]).name in ("bash", "sh", "zsh"):
    commit = commit or bool(re.search(r"\bgit\s+commit\b", command))
if not commit:
    sys.exit(0)
unsupported = "Stage the intended files first, then use plain git commit -m MESSAGE. The hook supports only staged commits without shell operators, expansions, Git global options, pathspecs, -a/--all, --include/--only or --amend."
if words[:2] != ["git", "commit"]:
    deny(unsupported)
# shlex removes quotes; inspect only shell syntax here, preserving literal messages.
quote = None
escaped = False
for char in command:
    if escaped:
        escaped = False
        continue
    if char == chr(92) and quote != chr(39):
        escaped = True
    elif char in (chr(39), chr(34)) and (quote is None or quote == char):
        quote = None if quote else char
    elif quote != chr(39) and char in "$`":
        deny(unsupported)
    elif quote is None and char in "\n;<>|&()":
        deny(unsupported)
args = iter(words[2:])
for arg in args:
    if arg in ("-m", "--message"):
        if next(args, None) is None:
            deny(unsupported)
    elif arg.startswith("--message=") or (arg.startswith("-m") and len(arg) > 2):
        continue
    elif arg not in ("-q", "--quiet", "-v", "--verbose", "--allow-empty",
                     "-n", "--no-verify", "-s", "--signoff"):
        deny(unsupported)
root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
if root.returncode:
    deny("Cannot locate repository for staged marketplace validation.")
result = subprocess.run(["bash", str(Path(root.stdout.strip()) / ".github/scripts/check-marketplace.sh"), "--staged"],
                        cwd=root.stdout.strip(), capture_output=True, text=True)
if result.returncode:
    deny("Marketplace staged check failed:\n" + result.stdout + result.stderr)
'
