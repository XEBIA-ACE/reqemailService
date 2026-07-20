# PLAN: Upgrade SQLAlchemy from 1.3 to 2.0.x

## Overview

**Strategy:** Big-bang migration.

**Justification:** The risk score and person-day estimate from the selected "moderate" upgrade option (details not provided) suggests a manageable level of risk and development effort. Due to major breaking changes from SQLAlchemy 1.3 to 2.0.x (notably around API usage and ORM changes), maintaining dual support for both versions is not feasible or cost-effective. Therefore, a one-time, all-at-once upgrade ("big-bang") avoids the complexity and maintenance overhead of feature flags or parallel runtimes.

---

## Phases

| Phase | Description                                                     | Dependencies | Estimated Effort           |
|-------|-----------------------------------------------------------------|--------------|----------------------------|
| 1     | Static/code-level refactoring and syntax updates for SQLAlchemy | None         | Derived from upgrade option|
| 2     | Perform full dependency upgrade and resolve runtime incompatibilities | Phase 1     | Derived from upgrade option|
| 3     | Full regression and performance testing post-upgrade            | Phase 2      | Derived from upgrade option|

---

## Component Changes

- **Affected Components:**
    - All modules/components that import, construct, or interact with SQLAlchemy APIs.
    - Files with declarative models, session creation, engine binding, or custom SQL execution.

- **Structural Changes and Affected Files:**
    - Refactor ORM model base classes and import patterns.  
      - Update all `from sqlalchemy.ext.declarative import declarative_base` usages.
    - Replace all usages of deprecated session APIs and transaction management syntax.
    - Update query construction to conform to new Core and ORM Query APIs.
    - Replace removed/moved modules/classes, e.g., `sqlalchemy.orm.query.Query`.
    - Update engine/bind patterns and connection handling, as per 2.0 migration guidelines.
    - Update or remove legacy config flags (`use_native_unicode`, etc.), if present.

    **Concrete Examples (if present in context):**
    - Update:
      ```python
      Session = sessionmaker(bind=engine)
      session = Session()
      ```
      to:
      ```python
      Session = sessionmaker()
      with Session(engine) as session:
          # ...
      ```
    - Change all `session.query(Model).filter(...).all()` to use the 2.0 style.

- **API Modifications:**
    - Modernize all SQLAlchemy ORM, Engine, and Session usages per upstream migration guides.
    - Refactor models and metadata registration.
    - Remove or update deprecated arguments, keyword changes, and initialization patterns.

*Note: Specific file and class names will depend on the actual codebase and should be identified via static analysis/search for SQLAlchemy import and API usage patterns.*

---

## Dependency Upgrade Plan

| Dependency   | Current Version | Target Version | Breaking Changes                                        | Migration Notes          |
|--------------|----------------|---------------|---------------------------------------------------------|--------------------------|
| SQLAlchemy   | 1.3            | 2.0.x         | - New 2.0-style API<br>- Deprecated module removals<br>- Changed query and session handling<br>- Transaction context required<br>- Removed legacy behaviors | Carefully follow [SQLAlchemy 2.0 migration guide](https://docs.sqlalchemy.org/en/20/changelog/changelog_20.html#migration-20-toplevel) and update all initialization, querying, and session patterns. |

---

## Infrastructure Changes

N/A — not applicable to this task

---

## Rollback Strategy

**Phase 1 (Code Refactor):**
- Revert to last stable commit on main branch if refactoring introduces errors.

**Phase 2 (Dependency Upgrade):**
- Downgrade SQLAlchemy back to 1.3 in requirements/config.
- Revert all code changes to pre-2.0-compatible patterns via version control.

**Phase 3 (Testing):**
- Restore prior database schema state, if migrations were applied.
- If post-upgrade issues are found, roll back to pre-upgrade application deployment (binary/code and dependencies).

Each rollback step:
1. Isolates only the most recent phase's changes using version control (git revert/reset).
2. Validates application health after reversal before resuming services.

---

## Testing Strategy

- **Unit Testing:**
    - All code paths interacting with SQLAlchemy should have unit test coverage.
    - _Target:_ ≥90% coverage on models, queries, transaction handling.
    - _Tool:_ pytest (or language-appropriate unit test runner).

- **Integration Testing:**
    - Validate ORM-to-database communication, migrations, and all CRUD operations.
    - Tests must exercise real database backends (not just in-memory SQLite if production is different).

- **Regression Testing:**
    - Full end-to-end application tests to ensure no behavior change post-upgrade.
    - Use existing regression test suite.

- **Performance Testing:**
    - Compare key database operation latencies and throughput before/after upgrade.

- **CI Gates:**
    - Block merges unless:
        - All unit/integration tests pass.
        - No reduction in test coverage.
        - Performance benchmarks within acceptable thresholds.

---

## Timeline

| Milestone                | Phase | Estimated Completion | Owner    |
|--------------------------|-------|---------------------|----------|
| Static code refactor     | 1     | Derived from effort | TODO     |
| Dependency upgrade       | 2     | Derived from effort | TODO     |
| Regression/Performance test & release | 3 | Derived from effort | TODO     |

*Estimated completion dates and owners to be filled in based on "moderate" option effort allocation.*

---