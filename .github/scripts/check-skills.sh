#!/usr/bin/env bash
#
# check-skills.sh - read-only structural checks for the skills tree.
#
# Replaces the former Python checker with shell and awk. It verifies:
#   - the installed skill catalog and its frontmatter;
#   - explicit-invocation policies;
#   - review role files;
#   - resource ownership, consumers and byte-identical shared copies;
#   - the fenced ticket Done when copy;
#   - ticket gates, checkpoint coverage and independent review structure;
#   - removed routes and mandatory setup journal injection stay absent;
#   - links stay inside the owning skill;
#   - no bundled link escapes an installed skill;
#   - CHANGELOG release headings keep their dated shape.
#
# Usage:
#   bash .github/scripts/check-skills.sh

set -uo pipefail

root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd) || exit 1
cd "$root" || exit 1

fail() {
  printf 'skills check: %s\n' "$1" >&2
  exit 1
}

SKILLS=(
  rnd-grill rnd-debug dev-exec dev-review dev-spec dev-commit nxs-setup
)
EXPLICIT=(
  rnd-grill rnd-debug dev-exec dev-review dev-spec nxs-setup
)
REMOVED=(
  rnd-map rnd-research rnd-prototype rnd-audit rnd-design
  to-decision to-spec to-questionnaire to-tickets to-handoff nxs-lead nxs-retro
)
ROLES=(
  review-quality review-testing review-simplification review-verify
)

# First consumer owns the resource. Single-owner rows require no duplicate
# copies; shared rows require exactly the listed consumers, byte-identical.
RESOURCES="
references/discussion.md|rnd-grill
references/domain-modeling.md|rnd-grill
references/evidence-methods.md|rnd-grill
references/prototype.md|rnd-grill
references/saving.md|rnd-grill
references/questionnaire.md|rnd-grill
references/writing-for-agents.md|nxs-setup
references/ticket.md|dev-exec
references/work-preparation.md|dev-exec
references/handoff.md|dev-exec
references/review-report.md|dev-review
references/selected-snapshot.md|dev-review
references/agent-launch.md|dev-review
references/findings.md|dev-review
references/project-specs.md|dev-spec,dev-review,rnd-grill,dev-exec,rnd-debug
assets/decision.md|rnd-grill
assets/spec.md|rnd-grill
assets/questionnaire.md|rnd-grill
assets/ticket.md|dev-exec
assets/handoff.md|dev-exec
assets/project-spec.md|dev-spec
"

frontmatter_field() {
  # Print one top-level frontmatter scalar, joining a block scalar.
  awk -v key="$2" '
    NR == 1 && $0 == "---" { fm = 1; next }
    fm && $0 == "---" { if (block) print text; done = 1; exit }
    !fm { next }
    index($0, key ":") == 1 {
      value = substr($0, length(key) + 2)
      sub(/^[ \t]+/, "", value)
      if (value ~ /^[>|][+-]?$/) { block = 1; next }
      if (key == "name" && value ~ /^"[^"]*"$/) value = substr(value, 2, length(value) - 2)
      if (key == "name" && value ~ /^\047[^\047]*\047$/) value = substr(value, 2, length(value) - 2)
      print value
      done = 1
      exit
    }
    block && /^[ \t]+/ { sub(/^[ \t]+/, ""); text = text (text == "" ? "" : " ") $0; next }
    block { print text; done = 1; exit }
    END { if (block && !done) print text }
  ' "$1"
}

check_frontmatter() {
  awk '
    function valid_quoted(value, quote,    i, c, nextc, hex) {
      for (i = 2; i <= length(value); i++) {
        c = substr(value, i, 1)
        if (c == quote) {
          if (quote == sq && substr(value, i + 1, 1) == sq) { i++; continue }
          return substr(value, i + 1) ~ /^[ \t]*(#.*)?$/
        }
        if (quote == "\"" && c == "\\") {
          nextc = substr(value, ++i, 1)
          if (nextc == "u") {
            hex = substr(value, i + 1, 4)
            if (length(hex) != 4 || hex !~ /^[[:xdigit:]]+$/) return 0
            i += 4
          } else if (index("\"\\/bfnrt", nextc) == 0 || nextc == "") return 0
        }
      }
      return 0
    }
    BEGIN { sq = sprintf("%c", 39) }
    NR == 1 { if ($0 != "---") exit 1; next }
    $0 == "---" { if (block && !block_content) exit 1; closed = 1; exit }
    block && /^[ ]+[^ ]/ {
      indent = match($0, /[^ ]/) - 1
      if (block_content && indent < block_indent) exit 1
      if (!block_content) block_indent = indent
      block_content = 1; next
    }
    block && /^[ \t]*$/ { next }
    block { if (!block_content) exit 1; block = 0 }
    /^[A-Za-z][A-Za-z0-9_-]*:/ {
      key = $0; sub(/:.*/, "", key)
      if (seen[key]++) exit 1
      value = substr($0, length(key) + 2); sub(/^[ \t]+/, "", value)
      if (value ~ /^[>|]/) {
        if (value !~ /^[>|][+-]?$/) exit 1
        block = 1; block_content = 0; next
      }
      first = substr(value, 1, 1)
      if (first == "\"" || first == sq) {
        if (!valid_quoted(value, first)) exit 1
        if ((key == "name" || key == "description") && value ~ ("^" first first "[ \t]*(#.*)?$")) exit 1
      } else if (value ~ /:[ \t]/ || value ~ /^[\[\]{}&*!%@`]/) exit 1
      else if ((key == "name" || key == "description") && value ~ /^(null|~|true|false)([ \t]*(#.*)?)?$/) exit 1
      next
    }
    /^[ \t]*($|#)/ { next }
    { exit 1 }
    END { if (!closed) exit 1 }
  ' "$1" || fail "$1: invalid, duplicate or unclosed frontmatter"
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
  local expected actual name
  [ "${#SKILLS[@]}" -eq 7 ] || fail "source catalog must have seven commands"
  [ "$(printf '%s\n' "${SKILLS[@]}" | sort -u | wc -l | tr -d ' ')" -eq 7 ] || fail "duplicate source command"
  [ "${#EXPLICIT[@]}" -eq 6 ] || fail "six commands must require explicit invocation"
  [ "$(printf '%s\n' "${EXPLICIT[@]}" | sort)" = "$(printf '%s\n' "${SKILLS[@]}" | grep -vx dev-commit | sort)" ] ||
    fail "only dev-commit may use direct commit-request invocation"
  actual=$(find skills -type l -print) || fail "cannot inspect skill symlinks"
  [ -z "$actual" ] || fail "source skills must bundle real files, not symlinks: $actual"
  expected=$(printf '%s\n' "${SKILLS[@]}" | sort)
  actual=$(find skills -mindepth 1 -maxdepth 1 -exec basename {} \; | sort) || fail "cannot read source catalog"
  [ "$expected" = "$actual" ] || fail "skills: expected [$(printf '%s ' "${SKILLS[@]}")], found [$(printf '%s ' $actual)]"
  expected=$(for name in "${SKILLS[@]}"; do printf 'skills/%s/SKILL.md\n' "$name"; done | sort)
  actual=$(find skills -type f -name SKILL.md | sort) || fail "cannot read command entry points"
  [ "$expected" = "$actual" ] || fail "unexpected or missing command entry point: $actual"
}

check_skill() {
  local name=$1 path fields name_value description policy allow
  path="skills/$name/SKILL.md"
  [ -f "$path" ] || fail "$path: missing required file"
  check_frontmatter "$path"
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
    allow=$(awk '
      /^policy:[ \t]*$/ { policies++; inside = 1; next }
      /^[^ \t#]/ { inside = 0 }
      inside && /^  allow_implicit_invocation:[ \t]*/ { values++; value = $2 }
      END { if (policies == 1 && values == 1) print value }
    ' "$policy")
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
    check_frontmatter "$path"
    [ "$(frontmatter_field "$path" name)" = "$role" ] || fail "$path: role name must match filename"
    [ -n "$(frontmatter_field "$path" description)" ] || fail "$path: missing or empty description frontmatter field"
    tools=$(frontmatter_field "$path" tools)
    declared=$(printf '%s' "$tools" | tr -d ' ' | tr ',' '\n' | sort | tr '\n' ' ')
    [ "$declared" = "Bash Glob Grep Read " ] || fail "$path: unexpected role tools"
    require_rule "$path" 'Только чтение:.*не меняй код' "read-only role boundary"
    require_rule "$path" 'Не пиши отчет и любые файлы, не меняй Git' "report/source write prohibition"
    require_rule "$path" 'source manifest.*точные history/diff/file/search reads' "selected-source context"
    require_link skills/dev-review/references/agent-launch.md "../roles/$role.md"
  done
}

check_shared() {
  local row relative consumers canonical consumer expected actual
  while IFS= read -r row; do
    [ -n "$row" ] || continue
    relative=${row%%|*}
    consumers=${row#*|}
    canonical="skills/${consumers%%,*}/$relative"
    [ -f "$canonical" ] || fail "$canonical: missing shared file"
    expected=$(printf '%s' "$consumers" | tr ',' '\n' | sort)
    actual=$(find skills -type f -path "skills/*/$relative" | awk -F/ '{ print $2 }' | sort) || fail "cannot inspect consumers of $relative"
    [ "$expected" = "$actual" ] || fail "$relative: expected consumers [$consumers], found [$actual]"
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
$RESOURCES
EOF
}

extract_done_when() {
  awk '
    /^## Условия завершения$/ { inside = 1; print; next }
    inside && /^#(#)? / { exit }
    inside { print }
  ' "$1"
}

extract_fenced_done_when() {
  awk '
    /^(`{3,}|~{3,})/ {
      if (!inside) { inside = 1; body = ""; next }
      inside = 0
      if (body ~ /^## Условия завершения\n/) { printf "%s", body; exit }
      next
    }
    inside { body = body $0 "\n" }
  ' "$1"
}

check_done_when() {
  local source=skills/dev-exec/assets/ticket.md copy expected actual
  for copy in skills/nxs-setup/assets/issue-tracker.md; do
  expected=$(extract_done_when "$source")
  [ -n "$expected" ] || fail "$source: missing Done when section"
  actual=$(extract_fenced_done_when "$copy")
  [ -n "$actual" ] || fail "$copy: missing fenced Done when block"
  [ "$(printf '%s' "$expected" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}')" = "$(printf '%s' "$actual" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}')" ] ||
    fail "$copy: fenced Done when block differs from $source; copy it verbatim"
  done
}

# These are source-contract assertions, not proof of agent behavior. Validate
# template shape, actual bundled dependency edges and safety gates together.
require_rule() {
  grep -Eq -- "$2" "$1" || fail "$1: missing $3"
}

require_link() {
  grep -Fq -- "]($2)" "$1" || fail "$1: missing bundled dependency $2"
}

check_headings() {
  local actual
  actual=$(awk '/^## / { print }' "$1")
  [ "$actual" = "$2" ] || fail "$1: unexpected section structure: $actual"
}

check_ticket_contract() {
  local template=skills/dev-exec/assets/ticket.md rules=skills/dev-exec/references/ticket.md
  local preparation=skills/dev-exec/references/work-preparation.md actual
  actual=$(awk '/^\*\*[^*]+:\*\*/ { sub(/:.*/, ""); print }' "$template")
  [ "$actual" = $'**What to build\n**Blocked by\n**Branch\n**Status' ] || fail "$template: incorrect ticket fields/order"
  require_rule "$template" '^# <NN>:' "numbered ticket title"
  require_rule "$template" '^\*\*Status:\*\* ready-for-agent$' "initial status"
  require_rule "$template" '^- \[ \] ' "unchecked acceptance criteria"
  check_headings "$template" '## Условия завершения'
  require_rule "$template" '^Выполни ticket напрямую через `/dev-exec <этот файл>`\.$' "executor handoff"
  require_rule "$template" '^- .*ready-for-agent.*Blocked by.*resolved.*проверенных результатах предпосылок.*выбранном рабочем дереве' "status and actual prerequisite gates"
  require_rule "$template" '^- .*одобренный конкретный план.*согласия.*точную цель.*native permissions.*ready-for-human' "plan and direct human-step approval gate"
  require_rule "$template" 'ready-for-agent.*проверь реальный результат; не повторяй действие с неизвестным эффектом' "human-step evidence and replay stop"
  require_rule "$template" '^- Закрывай только после каждого критерия, полного набора тестов проекта, линтера и остальных обязательных проверок:.*resolved' "verified completion gate"
  require_rule "$template" 'запрещенная/недоступная проверка оставляет ticket нерешенным' "missing-check stop"
  require_rule "$template" '^- Коммиты необязательны.*явного разрешения.*охват.*dev-commit.*Do not commit' "commit authorization and preservation"
  if grep -Eq -- '(^|[^[:alnum:]_-])/plan([^[:alnum:]_-]|$)' "$template" skills/dev-review/SKILL.md; then
    fail "current ticket template and review must not restore the removed /plan executor"
  fi
  require_link "$rules" '../assets/ticket.md'
  require_link "$preparation" 'ticket.md'
  require_link "$preparation" '../assets/ticket.md'
  require_link skills/dev-exec/SKILL.md 'references/work-preparation.md'
  require_rule "$rules" 'Копируй .*Условия завершения.*дословно' "verbatim execution block rule"
  require_rule "$rules" 'Существующие tickets сохраняют текст исполнения.*Done when.*Comments.*Do not commit' "legacy ticket preservation"
  require_rule "$preparation" 'Перед записью сверь изменения источника и цели; сохрани конкурентные правки' "concurrent ticket preservation"
}

check_workflow_contract() {
  local executor=skills/dev-exec/SKILL.md review=skills/dev-review/SKILL.md
  local snapshot=skills/dev-review/references/selected-snapshot.md spec=skills/dev-spec/SKILL.md
  local launch=skills/dev-review/references/agent-launch.md report=skills/dev-review/references/review-report.md path
  require_link "$executor" 'references/handoff.md'
  require_link skills/dev-exec/references/handoff.md '../assets/handoff.md'
  check_headings skills/dev-exec/assets/handoff.md $'## Принято\n## Открытые вопросы\n## Не проверено\n## Проверки\n## Текущие артефакты и следующий шаг'
  for path in "$executor" skills/dev-exec/references/handoff.md skills/dev-exec/assets/handoff.md "$spec" "$snapshot"; do
    require_rule "$path" 'pre-checkpoint HEAD' "checkpoint starting identity"
    require_rule "$path" 'commit.*parent OID' "checkpoint commit/parent identities"
    require_rule "$path" 'оставшиеся.*изменения|остаток|оставшийся.*задачи' "remaining-work coverage"
  done
  require_rule "$executor" 'Сначала выполни нужные проверки готового блока' "checked checkpoint boundary"
  require_rule "$executor" 'полную процедуру.*осмотр index.*сохранность чужих staged и working-tree правок' "checkpoint commit safety procedure"
  require_rule "$executor" 'Do not commit.*остается обязательным' "existing commit prohibition"
  require_rule "$spec" 'Непустой index не сужает охват до staged' "full-task spec scope"
  require_rule "$spec" 'Checkpoint на обычной базе не попадает в diff' "base-omitted checkpoint warning"
  require_rule "$spec" 'согласованная более ранняя baseline.*остановись incomplete' "earlier-baseline coverage stop"
  require_link "$review" 'references/selected-snapshot.md'
  require_link "$review" 'references/agent-launch.md'
  require_link "$review" 'references/review-report.md'
  require_link "$review" 'references/findings.md'
  require_rule "$snapshot" 'Обычный scope.*committed checkpoint.*staged, unstaged, untracked' "complete intended-work scope"
  require_rule "$snapshot" 'Staged-only допустим лишь явно, не по содержимому index' "no staged-first truncation"
  require_rule "$snapshot" 'checkpoint.*candidate base.*остановись для явно согласованной более ранней границы' "review baseline coverage stop"
  require_rule "$snapshot" 'Ancestry/список путей не доказывают покрытие' "net-change coverage evidence"
  require_rule "$snapshot" 'Заново проверь untracked/unstaged inventories' "working-source currency"
  require_rule "$launch" 'Три finder roles, затем один verifier только после всех их результатов' "independent verifier ordering"
  require_rule "$launch" 'Не сообщай роль/проверку-автора' "verifier independence"
  require_rule "$launch" 'Обязательно даже при host-enforced restrictions' "mandatory state comparison"
  require_rule "$launch" 'tracked, untracked, ignored файлы и каталоги' "whole-tree state capture"
  require_rule "$launch" 'Неполная baseline/сверка или любое различие останавливает проход incomplete' "failed-state-check stop"
  require_rule "$launch" 'не представляй prompt-only как техническую защиту' "honest permission reporting"
  require_rule "$review" 'сам не подтверждай, не опровергай и не удаляй кандидата' "orchestrator verdict boundary"
  require_rule "$review" 'не код, tickets, project specs, журнал, index, Git objects и коммиты' "report-only review writes"
  require_rule "$review" 'Предложи .*dev-exec.*прямо с отчетом и номерами, без обязательного ticket' "direct selected-finding handoff"
  require_rule "$review" 'согласие на исправление/план.*воспроизвести либо иначе подтвердить.*до правок' "correction approval and evidence"
  require_rule "$report" 'sweep: incomplete.*никогда не актуален' "incomplete report currency stop"
  require_rule skills/dev-commit/SKILL.md 'Другие группы staged и выбранный путь mixed.*Остановись до изменения index' "foreign-index mixed-path stop"
  require_rule skills/dev-commit/SKILL.md 'Байты рабочих файлов сохраняй неизменными на протяжении всей команды' "working-byte preservation"
  check_headings skills/rnd-grill/assets/spec.md $'## Проблема\n## Решение\n## Пользовательские сценарии\n## Решения по реализации\n## Решения по проверке\n## Вне задачи\n## Дополнительные заметки'
  check_headings skills/dev-spec/assets/project-spec.md $'## Цель\n## Архитектура\n## Назначение\n## Ответственность\n## Границы\n## Контракты\n## Известные ограничения\n## Обоснование'
  require_rule skills/dev-spec/references/project-specs.md 'Цель.*Архитектура.*Назначение.*Ответственность.*Границы.*Контракты.*Известные ограничения.*Обоснование' "Russian project-spec headings"
  require_rule skills/dev-spec/references/project-specs.md 'Для существующих файлов допустимы прежние соответствия:.*Goal.*Architecture' "legacy project-spec reading"
}

check_removed_surfaces() {
  local path pattern
  pattern=$(IFS='|'; printf '%s' "${REMOVED[*]}")
  while IFS= read -r path; do
    if grep -Eq -- "(^|[^[:alnum:]_-])($pattern)([^[:alnum:]_-]|$)|--to-tickets|ticket: proposed" "$path"; then
      fail "$path: removed command or review ticket-export route in active skill resource"
    fi
    case "$path" in
      */controlled-run.md|*/task-journal.md|skills/dev-review/assets/outcome.schema.json)
        fail "$path: removed coordination resource" ;;
    esac
  done < <(find skills -type f \( -name '*.md' -o -name '*.json' -o -name '*.yaml' \) | sort)
  for path in skills/nxs-setup/assets/*.md; do
    if grep -Eq -- 'Task journal:|decision\.log|JSONL|controlled-run|step_id|run_id|plan_hash' "$path"; then
      fail "$path: obsolete setup journal or coordination injection"
    fi
  done
  if grep -Eq -- 'app-server|stream-json|OPENCODE_PASSWORD|/api/(plugin|model|agent|skill)' skills/nxs-setup/references/readiness.md; then
    fail "readiness must not restore private client discovery transports"
  fi
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
    skill_root=${path#skills/}
    skill_root=skills/${skill_root%%/*}
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
      ' "$path" | awk '
        {
          line = $0
          while (match(line, /\]\([^)]*\)/)) {
            print substr(line, RSTART + 2, RLENGTH - 3)
            line = substr(line, RSTART + RLENGTH)
          }
          if ($0 ~ /^ *\[[^]]+\]:[ \t]*/) {
            sub(/^ *\[[^]]+\]:[ \t]*/, "")
            print
          }
        }
      '
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
  awk '
    function finish_release() {
      if (release && !body) { print "empty release entry: " heading > "/dev/stderr"; bad = 1 }
    }
    /^## / {
      finish_release(); release = 0; body = 0
      if ($0 ~ /^## \[Unreleased\]/) next
      if ($0 !~ /^## \[[^]]+\] - [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9][ \t]*$/) {
        print "invalid release heading: " $0 > "/dev/stderr"; bad = 1; next
      }
      heading = $0; date = $0; sub(/^.* - /, "", date); sub(/[ \t]*$/, "", date)
      split(date, parts, "-"); year = parts[1] + 0; month = parts[2] + 0; day = parts[3] + 0
      days = (month == 2 ? 28 + (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0)) : (month == 4 || month == 6 || month == 9 || month == 11 ? 30 : 31))
      if (year < 1 || month < 1 || month > 12 || day < 1 || day > days) {
        print "invalid release date: " date > "/dev/stderr"; bad = 1
      }
      release = 1; count++; next
    }
    release && $0 ~ /[^[:space:]]/ && $0 !~ /^#/ { body = 1 }
    END { finish_release(); if (!count) { print "no dated release entries" > "/dev/stderr"; bad = 1 }; exit bad }
  ' CHANGELOG.md || fail "CHANGELOG.md: invalid release entries"
}

check_catalog
for name in "${SKILLS[@]}"; do
  check_skill "$name"
done
check_roles
check_shared
check_done_when
check_ticket_contract
check_workflow_contract
check_removed_surfaces
check_links
check_runtime_paths
check_changelog

printf 'skills check: passed\n'
