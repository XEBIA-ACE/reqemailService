## Prerequisites

- [ ] [XS] Confirm access to repository containing all source files using SQLAlchemy 1.3
- [ ] [XS] Verify Python installation (version compatible with SQLAlchemy 2.0.x, e.g., Python 3.7+)
- [ ] [XS] Confirm pip is available (version 20.0+ recommended)
- [ ] [XS] Obtain maintainer/admin permissions for running and modifying tests
- [ ] [XS] Ensure access to existing continuous integration configuration files (e.g., .github/workflows, .travis.yml)
- [ ] [XS] Obtain list of files where SQLAlchemy 1.3 APIs are imported or invoked

## Phase 1 — Preparation

- [ ] [S] Create feature branch `upgrade/sqlalchemy-2.0` from latest main branch
- [ ] [S] Audit requirements.txt and/or pyproject.toml for existing SQLAlchemy pin (`sqlalchemy==1.3.*`)
- [ ] [S] Capture current test suite execution results as a baseline (save output of pytest/unittest/other runner)
- [ ] [S] Gather list of all models, queries, and ORM usages referencing SQLAlchemy in the codebase

## Phase 2 — Core Upgrade

- [ ] [XS] Change SQLAlchemy requirement from 1.3 to `sqlalchemy>=2.0,<2.1` in requirements.txt and/or pyproject.toml
- [ ] [M] Update all import statements for migrated or relocated SQLAlchemy 2.0 symbols in relevant source files
- [ ] [L] Refactor all usages of legacy ORM Session methods and connection patterns to 2.0 API in models and data access logic
- [ ] [L] Replace deprecated Query, filter, and execution patterns per SQLAlchemy 2.0 migration guide in all affected files
- [ ] [M] Update any string-based relationships to use class-based references in all model definitions
- [ ] [S] Refactor or remove use of .execute() on Engines/Connections as per 2.0 execution model changes

## Phase 3 — Testing & Validation

- [ ] [S] Re-install dependencies with updated SQLAlchemy in the development environment
- [ ] [M] Execute full test suite and capture results post-upgrade
- [ ] [S] Compare test results with pre-upgrade baseline to identify regressions
- [ ] [S] Increase test coverage for refactored queries and models if coverage has declined

## Phase 4 — CI/CD & Infrastructure

- [ ] [S] Update CI pipelines in .github/workflows or other CI config files to use Python and SQLAlchemy 2.0.x in testing matrix
- [ ] [XS] Verify that Dockerfile and bake/environment files (if present) use base images compatible with SQLAlchemy 2.0.x
- [ ] [XS] Ensure no hardcoded `sqlalchemy==1.3.*` versions exist in deployment scripts or IaC templates

## Phase 5 — Documentation & Rollout

- [ ] [S] Add SQLAlchemy 2.0 migration notes and updated requirements to CHANGELOG.md
- [ ] [S] Review and update RUNBOOK.md or operations docs to reflect modified startup or migration steps
- [ ] [XS] Document any known behavioral changes impacting downstream workflows due to SQLAlchemy upgrade
- [ ] [S] Monitor logs and error reports post-deployment for issues related to upgrade for at least one release cycle

---

N/A — not applicable to this task:
- Language- or runtime-specific tasks beyond SQLAlchemy upgrade
- Application-level or business logic refactors outside ORM upgrade scope
- Components or dependencies unrelated to SQLAlchemy
