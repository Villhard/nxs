#!/usr/bin/env bash
#
# lint-house-style.sh - house-style character linter for Markdown.
#
# Scans git-tracked Markdown files for forbidden Unicode characters and
# exits non-zero (printing "file:line: <reason>" for each hit) when any
# are found; exits 0 when clean.
#
# Forbidden:
#   em-dash          U+2014
#   en-dash          U+2013
#   horizontal bar   U+2015
#   minus sign       U+2212
#   left  single q.  U+2018
#   right single q.  U+2019
#   left  double q.  U+201C
#   right double q.  U+201D
#   left  angle q.   U+00AB
#   right angle q.   U+00BB
#
# House rule: use ASCII minus "-" and straight quotes only.
#
# Usage:
#   lint-house-style.sh              scan all git-tracked *.md files
#   lint-house-style.sh FILE [...]   scan the given files (used by tests)
#
# This script source is pure ASCII on purpose: the forbidden set is built
# at runtime from raw UTF-8 byte escapes (printf octal), never from literal
# forbidden characters, so the linter can never flag itself.

set -u

# Build each forbidden character from its UTF-8 byte sequence via octal
# escapes. Octal escapes are byte-level and locale-independent, so the
# script source stays ASCII-only and portable across printf builds.
CH_EMDASH=$(printf '\342\200\224')   # U+2014 E2 80 94
CH_ENDASH=$(printf '\342\200\223')   # U+2013 E2 80 93
CH_HBAR=$(printf '\342\200\225')     # U+2015 E2 80 95
CH_MINUS=$(printf '\342\210\222')    # U+2212 E2 88 92
CH_LSQUO=$(printf '\342\200\230')    # U+2018 E2 80 98
CH_RSQUO=$(printf '\342\200\231')    # U+2019 E2 80 99
CH_LDQUO=$(printf '\342\200\234')    # U+201C E2 80 9C
CH_RDQUO=$(printf '\342\200\235')    # U+201D E2 80 9D
CH_LAQUO=$(printf '\302\253')        # U+00AB C2 AB
CH_RAQUO=$(printf '\302\273')        # U+00BB C2 BB

# Parallel arrays: forbidden char -> human reason.
CHARS=(
  "$CH_EMDASH" "$CH_ENDASH" "$CH_HBAR"  "$CH_MINUS"
  "$CH_LSQUO"  "$CH_RSQUO"  "$CH_LDQUO" "$CH_RDQUO"
  "$CH_LAQUO"  "$CH_RAQUO"
)
REASONS=(
  "em-dash (U+2014)" "en-dash (U+2013)" "horizontal bar (U+2015)" "minus sign (U+2212)"
  "left single quote (U+2018)" "right single quote (U+2019)"
  "left double quote (U+201C)" "right double quote (U+201D)"
  "left angle quote (U+00AB)" "right angle quote (U+00BB)"
)

# scan_file FILE -> prints "FILE:LINE: reason" for each hit.
# Returns 1 if any forbidden character was found, 0 if clean.
scan_file() {
  file="$1"
  found=0
  i=0
  while [ "$i" -lt "${#CHARS[@]}" ]; do
    ch="${CHARS[$i]}"
    reason="${REASONS[$i]}"
    # LC_ALL=C makes grep byte-oriented so the raw UTF-8 byte sequence is
    # matched exactly. grep -n gives "LINE:content"; we keep the line only.
    while IFS=: read -r lineno _; do
      [ -n "$lineno" ] || continue
      printf '%s:%s: %s\n' "$file" "$lineno" "$reason"
      found=1
    done < <(LC_ALL=C grep -nF -e "$ch" "$file" 2>/dev/null)
    i=$((i + 1))
  done
  return "$found"
}

main() {
  files=()
  if [ "$#" -gt 0 ]; then
    files=("$@")
  else
    while IFS= read -r f; do
      [ -n "$f" ] && files+=("$f")
    done < <(git ls-files '*.md')
  fi

  status=0
  for f in "${files[@]:-}"; do
    [ -n "$f" ] || continue
    [ -f "$f" ] || continue
    scan_file "$f" || status=1
  done
  return "$status"
}

main "$@"
