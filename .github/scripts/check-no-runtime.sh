#!/usr/bin/env bash
#
# check-no-runtime.sh - reject the removed Python runtime and agterm coupling.
#
# Active skills, guides and scenarios must not require Python 3, agterm or
# bundled .py helpers. Historical records (CHANGELOG.md and docs/adr/) keep
# their original text.
#
# Usage:
#   bash .github/scripts/check-no-runtime.sh

set -u

root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd) || exit 1
cd "$root" || exit 1

status=0

while IFS= read -r path; do
  printf 'runtime guard: unexpected Python file %s\n' "$path" >&2
  status=1
done < <(find . -path ./.git -prune -o -path ./.scratch -prune -o -path ./node_modules -prune -o -type f -name '*.py' -print)

while IFS= read -r path; do
  printf 'runtime guard: bundled script directory %s\n' "$path" >&2
  status=1
done < <(find skills -type d \( -name scripts -o -name __pycache__ \) -print)

ACTIVE=(
  README.md
  CONTRIBUTING.md
  SPEC.md
  GLOSSARY.md
  tests/client-scenarios.md
)
while IFS= read -r path; do
  ACTIVE+=("$path")
done < <(find docs -maxdepth 1 -type f -name '*.md' | sort)

while IFS= read -r path; do
  ACTIVE+=("$path")
done < <(find skills -type f \( -name '*.md' -o -name '*.json' -o -name '*.yaml' \) | sort)

for path in "${ACTIVE[@]}"; do
  [ -f "$path" ] || continue
  while IFS=: read -r line _; do
    [ -n "$line" ] || continue
    printf 'runtime guard: %s:%s names removed Python or agterm coupling\n' "$path" "$line" >&2
    status=1
  done < <(grep -nE 'python3|agterm|journal\.py|runner\.py|inventory\.py|approval\.py|status\.py|harness\.py|mechanics\.py|outcome\.py|scripts/[[:alnum:]_.-]+\.py' "$path")
done

if [ "$status" -ne 0 ]; then
  printf 'runtime guard: failed\n' >&2
  exit 1
fi

printf 'runtime guard: passed\n'
