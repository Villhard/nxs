#!/usr/bin/env bash
# Open a pending artifact in revdiff and print the annotations it captured.
#
# usage:
#   launch-artifact-review.sh <pending-file> <label>                  single revision
#   launch-artifact-review.sh <pending-file> <label> <baseline-file>  compare against a baseline
#
# stdout: the annotations, empty when the user left none
# exit:   0 clean, 10 annotations captured, anything else a launcher failure
#
# The pending file is a temp snapshot of content that has not been written yet,
# so <label> carries the real artifact path for the overlay title.

set -euo pipefail

sq() { printf "'%s'" "$(printf '%s' "$1" | sed "s/'/'\\\\''/g")"; }

PENDING="${1:-}"
LABEL="${2:-}"
BASELINE="${3:-}"

if [ -z "$PENDING" ] || [ -z "$LABEL" ]; then
    echo "usage: launch-artifact-review.sh <pending-file> <label> [baseline-file]" >&2
    exit 1
fi
if [ ! -f "$PENDING" ]; then
    echo "error: file not found: $PENDING" >&2
    exit 1
fi

abspath() { (cd "$(dirname "$1")" && printf '%s/%s\n' "$(pwd)" "$(basename "$1")"); }
PENDING_ABS=$(abspath "$PENDING")

COMPARE_MODE=0
if [ -n "$BASELINE" ]; then
    if [ ! -f "$BASELINE" ]; then
        echo "error: file not found: $BASELINE" >&2
        exit 1
    fi
    BASELINE_ABS=$(abspath "$BASELINE")
    REVDIFF_ARGS="$(sq "--compare-old=$BASELINE_ABS") $(sq "--compare-new=$PENDING_ABS")"
    COMPARE_MODE=1
else
    REVDIFF_ARGS="$(sq "--only=$PENDING_ABS")"
fi

REVDIFF_BIN=$(command -v revdiff 2>/dev/null || true)
if [ -z "$REVDIFF_BIN" ]; then
    echo "error: revdiff not found in PATH" >&2
    exit 1
fi

TMPBASE="${TMPDIR:-/tmp}"
CWD="$(pwd)"
OUTPUT_FILE=$(mktemp "$TMPBASE/gate-review-output-XXXXXX")
trap 'rm -f "$OUTPUT_FILE"' EXIT

# The exit-code-on-annotations switch travels as an env var rather than a flag:
# an older revdiff ignores an unknown env var and hard-fails on an unknown flag.
REVDIFF_CMD="REVDIFF_EXIT_CODE_ON_ANNOTATIONS=true $(sq "$REVDIFF_BIN") $REVDIFF_ARGS $(sq "--output=$OUTPUT_FILE") $(sq --wrap)"
# Collapsed compare reads as the new state with the changed lines highlighted,
# which is what a revision round calls for. A first draft is read whole.
if [ "$COMPARE_MODE" = "1" ]; then
    REVDIFF_CMD="$REVDIFF_CMD $(sq --collapsed)"
fi
OVERLAY_TITLE="artifact: $LABEL"

# agterm: `session overlay open --block` runs revdiff over the agent's own pane
# and blocks until it exits, so no sentinel file is needed. The session status
# goes to blocked while the overlay is up and back to active on every exit path.
if [ -n "${AGTERM_SESSION_ID:-}" ] && command -v agtermctl >/dev/null 2>&1; then
    AGTERM_TARGET=(--target "$AGTERM_SESSION_ID")
    [ -n "${AGTERM_SOCKET:-}" ] && AGTERM_TARGET+=(--socket "$AGTERM_SOCKET")
    AGTERM_STATUS=(session status blocked --blink)
    case "${AGTERM_PANE:-}" in
        left|right|scratch) AGTERM_STATUS+=(--pane "$AGTERM_PANE") ;;
    esac
    agtermctl "${AGTERM_STATUS[@]}" "${AGTERM_TARGET[@]}" >/dev/null 2>&1 || true
    trap 'agtermctl session status active "${AGTERM_TARGET[@]}" >/dev/null 2>&1 || true; rm -f "$OUTPUT_FILE"' EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
    rc=0
    agtermctl session overlay open "$REVDIFF_CMD" "${AGTERM_TARGET[@]}" --cwd "$CWD" --block >/dev/null || rc=$?
    cat "$OUTPUT_FILE"
    exit "$rc"
fi

# tmux: display-popup -E blocks until the command exits.
if [ -n "${TMUX:-}" ] && command -v tmux >/dev/null 2>&1; then
    TMUX_ARGS=(tmux display-popup -E -w 90% -h 90%)
    if [[ "$(tmux -V 2>/dev/null)" =~ ([0-9]+)\.([0-9]+) ]]; then
        if [ "${BASH_REMATCH[1]}" -gt 3 ] || { [ "${BASH_REMATCH[1]}" -eq 3 ] && [ "${BASH_REMATCH[2]}" -ge 3 ]; }; then
            TMUX_ARGS+=(-T " $OVERLAY_TITLE ")
        fi
    fi
    TMUX_ARGS+=(-- sh -c "$REVDIFF_CMD")
    rc=0
    "${TMUX_ARGS[@]}" || rc=$?
    cat "$OUTPUT_FILE"
    exit "$rc"
fi

echo "error: no overlay terminal available (this launcher handles agterm and tmux; see the README on overriding it)" >&2
exit 1
