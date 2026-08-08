# Summary

<!-- One line: what this PR changes and why. -->

## Checklist

- [ ] PUBLIC SAFETY: no `/Users/...` paths, real emails, tracker keys, or secrets in committed docs / artifacts
- [ ] Ran `claude plugin validate --strict .` and `claude plugin validate --strict plugins/<name>` for every touched plugin
- [ ] Ran `bash .github/scripts/lint-house-style.sh` locally and it is clean
- [ ] Bumped `version` and added a `CHANGELOG.md` entry in every touched plugin
