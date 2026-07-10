# Changelog

All notable changes to the `nxs` plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Publishable hardening: MIT `LICENSE`, plugin metadata (license, repository, homepage), this `CHANGELOG.md`, and a versioning convention in `CONTRIBUTING.md`.

## [0.3.0] - 2026-07-09

### Added

- `/nxs:epic` entry point for foggy, multi-session efforts.
- Fowler code-smell baseline in the review quality and simplification lenses.

## [0.2.0] - 2026-07-08

### Changed

- Single-source protocol model: the orchestrator injects one protocol kernel into every lens agent instead of each agent restating it.
- Deduped the review and plancheck lens agents against the injected protocol; each agent keeps only a guard line plus its domain content.
- Extracted shared kernels: adversarial stress-test, doc-draft contract, TDD cycle, and the bug diagnosis loop.
- Switched skills to a tool-agnostic "tracker" instead of naming a specific issue tracker.

## [0.1.0] - 2026-07-06

### Added

- Initial release: flat `/nxs:*` command skills (`plan`, `exec`, `review`, `plancheck`, `bug`, `rnd`, `dialectic`, `wrong`, `explain`, `userdoc`, `techdoc`, `recommit`, `clean`).
- Background (tier 3) rule skills loaded by relevance.
- Autonomous read-only agents for the review and plan lenses.
