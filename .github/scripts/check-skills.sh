#!/usr/bin/env bash
#
# check-skills.sh - read-only structural checks for the skills tree.
#
# Replaces the former Python checker with shell and awk. It verifies:
#   - the installed skill catalog and its frontmatter;
#   - explicit-invocation policies;
#   - review role files;
#   - byte-identical shared resources;
#   - the fenced ticket Done when copy;
#   - links stay inside the owning skill;
#   - no bundled link escapes an installed skill;
#   - CHANGELOG release headings keep their dated shape.
#
# Usage:
#   bash .github/scripts/check-skills.sh

set -u

root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd) || exit 1
cd "$root" || exit 1

fail() {
  printf 'skills check: %s\n' "$1" >&2
  exit 1
}

SKILLS=(
  dev-rnd dev-bug dev-review dev-spec dev-setup dev-commit dev-lead
  rnd-grill rnd-debug rnd-research rnd-prototype rnd-design rnd-audit to-decision to-spec to-tickets dev-exec
)
EXPLICIT=(
  dev-rnd dev-bug dev-review dev-spec dev-setup dev-lead
  rnd-grill rnd-debug rnd-research rnd-prototype rnd-design rnd-audit to-decision to-spec to-tickets dev-exec
)
ROLES=(
  review-quality review-testing review-simplification review-verify
)

# Files copied into every consuming skill and required to stay byte-identical.
# The canonical copy is the first consumer.
SHARED="
references/discussion.md|rnd-grill,to-decision,to-spec,rnd-design
references/domain-modeling.md|rnd-grill,to-decision,rnd-design
references/ticket.md|to-tickets,dev-rnd,dev-bug,dev-review,dev-exec
references/review-report.md|dev-review,to-tickets
references/feature-directory.md|dev-rnd,dev-bug,rnd-debug
references/project-specs.md|dev-rnd,dev-bug,dev-review,dev-spec,dev-lead,rnd-grill,to-decision,to-spec,to-tickets,dev-exec,rnd-debug,rnd-research,rnd-prototype,rnd-design,rnd-audit
references/task-journal.md|dev-lead,dev-rnd,dev-bug,dev-review,dev-spec,dev-commit,rnd-grill,to-decision,to-spec,to-tickets,dev-exec,rnd-debug,rnd-research,rnd-prototype,rnd-design,rnd-audit
references/controlled-run.md|dev-lead,dev-rnd,dev-bug,dev-review,dev-spec,dev-commit,rnd-grill,to-decision,to-spec,to-tickets,dev-exec,rnd-debug,rnd-research,rnd-prototype,rnd-design,rnd-audit
assets/spec.md|to-spec,dev-rnd,dev-bug,rnd-debug
assets/ticket.md|to-tickets,dev-rnd,dev-bug,dev-review,dev-exec
assets/outcome.schema.json|dev-lead,dev-review
"

frontmatter_field() {
  # Print one top-level frontmatter scalar, joining a block scalar.
  awk -v key="$2" '
    NR == 1 && $0 == "---" { fm = 1; next }
    fm && $0 == "---" { done = 1; exit }
    !fm { next }
    index($0, key ":") == 1 {
      value = substr($0, length(key) + 2)
      sub(/^[ \t]+/, "", value)
      if (value ~ /^[>|][+-]?$/) { block = 1; next }
      print value
      done = 1
      exit
    }
    block && /^[ \t]+/ { sub(/^[ \t]+/, ""); text = text (text == "" ? "" : " ") $0; next }
    block { print text; done = 1; exit }
    END { if (block && !done) print text }
  ' "$1"
}

frontmatter_has() {
  awk -v key="$2" '
    NR == 1 && $0 == "---" { fm = 1; next }
    fm && $0 == "---" { exit }
    fm && index($0, key ":") == 1 { found = 1; exit }
    END { exit !found }
  ' "$1"
}

is_explicit() {
  local name=$1 candidate
  for candidate in "${EXPLICIT[@]}"; do
    [ "$candidate" = "$name" ] && return 0
  done
  return 1
}

check_catalog() {
  local expected actual
  expected=$(printf '%s\n' "${SKILLS[@]}" | sort)
  actual=$(find skills -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort)
  [ "$expected" = "$actual" ] || fail "skills: expected [$(printf '%s ' "${SKILLS[@]}")], found [$(printf '%s ' $actual)]"
}

check_skill() {
  local name=$1 path fields name_value description policy allow
  path="skills/$name/SKILL.md"
  [ -f "$path" ] || fail "$path: missing required file"
  name_value=$(frontmatter_field "$path" name)
  [ "$name_value" = "$name" ] || fail "$path: name must match directory $name"
  description=$(frontmatter_field "$path" description)
  [ -n "$(printf '%s' "$description" | tr -d '[:space:]')" ] || fail "$path: missing or empty description frontmatter field"
  [ "${#description}" -le 1024 ] || fail "$path: description exceeds 1024 characters"

  if frontmatter_has "$path" disable-model-invocation; then
    case $(frontmatter_field "$path" disable-model-invocation) in
      true|false) ;;
      *) fail "$path: disable-model-invocation must be an unquoted boolean" ;;
    esac
  fi

  if is_explicit "$name"; then
    [ "$(frontmatter_field "$path" disable-model-invocation)" = true ] || fail "$path: incorrect invocation policy"
  else
    [ "$(frontmatter_field "$path" disable-model-invocation)" != true ] || fail "$path: incorrect invocation policy"
  fi

  policy="skills/$name/agents/openai.yaml"
  if is_explicit "$name" || [ -f "$policy" ]; then
    [ -f "$policy" ] || fail "$policy: missing required file"
    allow=$(awk '/^[ ]{2}allow_implicit_invocation:/ { print $2; exit }' "$policy")
    if is_explicit "$name"; then
      [ "$allow" = false ] || fail "$policy: incorrect invocation policy"
    else
      [ "$allow" = true ] || fail "$policy: incorrect invocation policy"
    fi
  fi
}

check_roles() {
  local expected actual role path tools declared
  expected=$(printf '%s\n' "${ROLES[@]}" | sort)
  actual=$(find skills/dev-review/roles -mindepth 1 -maxdepth 1 -name '*.md' -exec basename {} .md \; | sort)
  [ "$expected" = "$actual" ] || fail "skills/dev-review/roles: expected [${ROLES[*]}], found [$actual]"
  for role in "${ROLES[@]}"; do
    path="skills/dev-review/roles/$role.md"
    [ "$(frontmatter_field "$path" name)" = "$role" ] || fail "$path: role name must match filename"
    [ -n "$(frontmatter_field "$path" description)" ] || fail "$path: missing or empty description frontmatter field"
    tools=$(frontmatter_field "$path" tools)
    declared=$(printf '%s' "$tools" | tr -d ' ' | tr ',' '\n' | sort -u | tr '\n' ' ')
    [ "$declared" = "Bash Glob Grep Read " ] || fail "$path: unexpected role tools"
  done
}

check_shared() {
  local row relative consumers canonical consumer
  while IFS= read -r row; do
    [ -n "$row" ] || continue
    relative=${row%%|*}
    consumers=${row#*|}
    canonical="skills/${consumers%%,*}/$relative"
    [ -f "$canonical" ] || fail "$canonical: missing shared file"
    local rest=${consumers#*,}
    [ "$rest" = "$consumers" ] && continue
    local old_ifs=$IFS
    IFS=,
    for consumer in $rest; do
      IFS=$old_ifs
      [ -f "skills/$consumer/$relative" ] || fail "skills/$consumer/$relative: missing shared file"
      cmp -s "$canonical" "skills/$consumer/$relative" || fail "skills/$consumer/$relative: shared file differs from $canonical; propagate the copy"
    done
    IFS=$old_ifs
  done <<EOF
$SHARED
EOF
}

extract_done_when() {
  awk '
    /^## Done when$/ { inside = 1; print; next }
    inside && /^#{1,2} / { exit }
    inside { print }
  ' "$1"
}

extract_fenced_done_when() {
  awk '
    /^(`{3,}|~{3,})/ {
      if (!inside) { inside = 1; body = ""; next }
      inside = 0
      if (body ~ /^## Done when\n/) { printf "%s", body; exit }
      next
    }
    inside { body = body $0 "\n" }
  ' "$1"
}

check_done_when() {
  local source=skills/to-tickets/assets/ticket.md copy=skills/dev-setup/assets/issue-tracker.md expected actual
  expected=$(extract_done_when "$source")
  [ -n "$expected" ] || fail "$source: missing Done when section"
  actual=$(extract_fenced_done_when "$copy")
  [ -n "$actual" ] || fail "$copy: missing fenced Done when block"
  [ "$(printf '%s' "$expected" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}')" = "$(printf '%s' "$actual" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}')" ] ||
    fail "$copy: fenced Done when block differs from $source; copy it verbatim"
}

normalize_path() {
  local path=$1 part
  local -a parts out
  IFS=/ read -r -a parts <<< "$path"
  for part in "${parts[@]}"; do
    case $part in
      ''|.) ;;
      ..) unset 'out[${#out[@]}-1]' 2>/dev/null || true ;;
      *) out+=("$part") ;;
    esac
  done
  IFS=/
  printf '%s' "${out[*]}"
}

check_links() {
  local path skill_root destination target
  while IFS= read -r path; do
    skill_root=skills/${path#skills/}
    skill_root=${skill_root%%/*}
    while IFS= read -r destination; do
      case $destination in
        http://*|https://*|mailto:*|\#*|'') continue ;;
      esac
      destination=${destination#<}
      destination=${destination%>}
      destination=${destination%%#*}
      destination=${destination%% *}
      [ -n "$destination" ] || continue
      target=$(normalize_path "${path%/*}/$destination")
      case $target in
        "$skill_root"/*) ;;
        *) fail "$path: bundled Markdown resource escapes its skill: $destination" ;;
      esac
      [ -e "$target" ] || fail "$path: missing local Markdown resource $destination ($target)"
    done < <(
      awk '
        /^[ \t]*(```|~~~)/ { fence = !fence; next }
        fence { next }
        { gsub(/`[^`]*`/, ""); print }
      ' "$path" | grep -oE '\]\([^)]*\)' | sed -e 's/^](//' -e 's/)$//'
    )
  done < <(find skills -type f -name '*.md' | sort)
}

check_runtime_paths() {
  local path
  while IFS= read -r path; do
    if grep -Eq '(\.\./)+(skills/)?(dev|rnd|to|nxs)-[a-z-]+/' "$path"; then
      fail "$path: external runtime skill reference"
    fi
    if grep -Eq '/(Users|home)/[^/[:space:]]+/([^[:space:]]*/)?(skills|\.codex|\.agents)/' "$path"; then
      fail "$path: external installed runtime path"
    fi
  done < <(find skills -type f \( -name '*.md' -o -name '*.json' -o -name '*.yaml' \) | sort)
}

check_changelog() {
  grep -Eq '^## \[[^]]+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}[ \t]*$' CHANGELOG.md ||
    fail "CHANGELOG.md: no dated release entries"
}

check_catalog
for name in "${SKILLS[@]}"; do
  check_skill "$name"
done
check_roles
check_shared
check_done_when
check_links
check_runtime_paths
check_changelog

printf 'skills check: passed\n'
