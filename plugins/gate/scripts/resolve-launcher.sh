#!/usr/bin/env bash
# Resolve a launcher script through the override chain: user layer, then bundled.
# usage: resolve-launcher.sh <launcher-name> [data-dir]
# Prints the absolute path of the first executable launcher found.
#
# There is no project (.claude/...) layer on purpose. The hook fires
# automatically in any repository this runtime opens, and a repo-controlled
# executable layer would let an untrusted checkout run arbitrary code on a
# routine Write.
set -euo pipefail

name="${1:-}"
if [ -z "$name" ]; then
    echo "error: usage: resolve-launcher.sh <launcher-name> [data-dir]" >&2
    exit 1
fi
data_dir="${2:-${CLAUDE_PLUGIN_DATA:-}}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

abspath() { (cd "$(dirname "$1")" && printf '%s/%s\n' "$(pwd)" "$(basename "$1")"); }

if [ -n "$data_dir" ] && [ -f "$data_dir/scripts/$name" ] && [ -x "$data_dir/scripts/$name" ]; then
    abspath "$data_dir/scripts/$name"
    exit 0
fi
if [ -f "$SCRIPT_DIR/$name" ] && [ -x "$SCRIPT_DIR/$name" ]; then
    abspath "$SCRIPT_DIR/$name"
    exit 0
fi
echo "error: launcher not found in override chain: $name" >&2
exit 1
