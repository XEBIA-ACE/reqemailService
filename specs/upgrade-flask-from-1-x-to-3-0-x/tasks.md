# TASKS: Flask 1.x → 3.0.x Modernization

## Prerequisites

- [ ] [XS] Ensure access to project repository on GitHub (access control list: core team)
- [ ] [XS] Install Python >=3.8 on local and CI environments (per Flask 3.0.x requirements)
- [ ] [XS] Install pip >=21.0 for modern dependency resolution
- [ ] [XS] Verify write access to requirements.txt file in repo root
- [ ] [XS] Obtain ability to create and push feature branches
- [ ] [XS] Confirm ability to run test suite locally (pytest, unittest, or as configured)

## Phase 1 — Preparation

- [ ] [XS] Create feature branch `upgrade/flask-3` from current main branch
- [ ] [S] Audit requirements.txt for Flask and related/extension dependencies (Flask-*, Werkzeug, Jinja2, etc.)
- [ ] [XS] Capture current test suite results as baseline by running `pytest` or existing test runner and storing results as `tests/baseline_flask1.json`
- [ ] [XS] Identify and document any Flask 1.x deprecations or known incompatibilities in `docs/upgrade/flask3_incompatibilities.md`

## Phase 2 — Core Upgrade

- [ ] [XS] Upgrade Flask from 1.x to 3.0.x in requirements.txt
- [ ] [S] Audit and upgrade Werkzeug, Jinja2, MarkupSafe, and other Flask direct dependencies in requirements.txt to versions compatible with Flask 3.0.x
- [ ] [M] Update imports, removed APIs, and incompatibilities in all Python modules in `app/` (per Flask 3.0 migration notes)
- [ ] [S] Replace usage of removed `app.json_encoder/app.json_decoder` in `app/main.py` (if present)
- [ ] [S] Refactor `app/request_handlers.py` to address usage of deprecated `request.is_xxx` attributes removed in Flask 3.x
- [ ] [S] Update custom error handlers in `app/errors.py` to align with Flask 3.0 exception handling changes
- [ ] [S] Refactor blueprint registration usage in `app/routes.py` to match Flask 3.0+ signature requirements

## Phase 3 — Testing & Validation

- [ ] [M] Run complete test suite in upgraded environment; capture output as `tests/flask3_upgrade_results.json`
- [ ] [XS] Compare `tests/flask3_upgrade_results.json` with `tests/baseline_flask1.json` to identify regressions
- [ ] [XS] Verify test coverage is unchanged using `coverage report` (if enabled in project)
- [ ] [S] Remediate all failed tests in `app/` that were passing in the Flask 1.x baseline

## Phase 4 — CI/CD & Infrastructure

- [ ] [XS] Update CI workflow file `.github/workflows/ci.yml` to reference Python >=3.8
- [ ] [XS] Update Dockerfile (if present) to install Flask 3.0.x and Python >=3.8 explicitly
- [ ] [XS] Validate Docker image builds and runs successfully with Flask 3.0.x

## Phase 5 — Documentation & Rollout

- [ ] [XS] Update `docs/CHANGELOG.md` with Flask 3.0.x upgrade details and notable migration changes
- [ ] [XS] Review and update runbook sections referencing Flask APIs in `docs/RUNBOOK.md`
- [ ] [XS] Prepare and communicate rollout/merge plan to team, schedule staged deployment as per existing policy
- [ ] [XS] Set up post-deployment monitoring in `docs/upgrade/flask3_monitoring.md` (include key Flask 3 error patterns to watch)

---

**End of Tasks.**