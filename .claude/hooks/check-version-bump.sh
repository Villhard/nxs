#!/usr/bin/env bash
# PreToolUse/Bash hook. Blocks a commit that edits a plugin's bundled content
# without bumping that plugin's version and logging the change, the rule in
# CONTRIBUTING.md "VERSIONING". Reads the hook payload on stdin, writes a deny
# decision on stdout, and stays silent for every command that is not a commit.
set -uo pipefail

payload=$(cat)
command=$(printf '%s' "$payload" | jq -r '.tool_input.command // ""')

case "$command" in
  *"git commit"*) ;;
  *) exit 0 ;;
esac

root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$root" || exit 0

files=$(git diff --cached --name-only)

# -a and -am stage every tracked change at commit time, so those files are part
# of the commit even though they are not in the index yet.
case "$command" in
  *" -a"*|*" --all"*) files=$(printf '%s\n%s' "$files" "$(git diff --name-only)") ;;
esac

plugins=$(printf '%s\n' "$files" | sed -n 's#^plugins/\([^/]*\)/.*#\1#p' | sort -u)
[ -z "$plugins" ] && exit 0

missing=""
for plugin in $plugins; do
  manifest="plugins/$plugin/.claude-plugin/plugin.json"
  changelog="plugins/$plugin/CHANGELOG.md"

  # Content only. A commit touching the manifest or the changelog alone is a
  # release commit or a changelog fix, and neither owes a bump.
  content=$(printf '%s\n' "$files" | grep "^plugins/$plugin/" | grep -v -e "^$manifest\$" -e "^$changelog\$")
  [ -z "$content" ] && continue

  lacks=""
  printf '%s\n' "$files" | grep -qx "$manifest" || lacks="$manifest"
  printf '%s\n' "$files" | grep -qx "$changelog" || lacks="${lacks:+$lacks and }$changelog"
  [ -n "$lacks" ] && missing="${missing}The commit edits $plugin but does not stage $lacks. "
done

[ -z "$missing" ] && exit 0

jq -n --arg reason "${missing}CONTRIBUTING.md: every edit to bundled content bumps the version in plugin.json and adds a CHANGELOG.md entry, in the same change. Patch when the contract is untouched, minor when it changed - plugins/<name>/CONTRIBUTING.md defines the contract." \
  '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: $reason}}'
