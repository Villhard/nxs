#!/usr/bin/env bash
# SessionStart hook for the dev plugin - inject the using-dev discipline.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
discipline_content=$(cat "${SCRIPT_DIR}/using-dev.md" 2>&1 || echo "Error reading using-dev.md")

# Escape a string for JSON embedding via bash parameter substitution.
escape_for_json() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

discipline_escaped=$(escape_for_json "$discipline_content")
context="You have the dev plugin. The 'using-dev' discipline below is standing guidance for this session - follow it. For dev skills, use the 'Skill' tool.\n\n${discipline_escaped}"

# Claude Code reads hookSpecificOutput.additionalContext.
printf '{\n  "hookSpecificOutput": {\n    "hookEventName": "SessionStart",\n    "additionalContext": "%s"\n  }\n}\n' "$context"

exit 0
