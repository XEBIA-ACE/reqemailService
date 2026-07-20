## Summary

This specification covers the direct upgrade of SQLAlchemy from version 1.3 to 2.0.x within the project ecosystem. The expected outcome is to have all application components and dependencies compatible with SQLAlchemy 2.0.x, with deprecated APIs removed, compatibility layers addressed, and breaking changes resolved, allowing uninterrupted and maintainable data access.

## Motivation

Upgrading SQLAlchemy from 1.3 to 2.0.x is necessary due to the following drivers:
- **End of Life (EOL):** SQLAlchemy 1.3 has reached or is near EOL, lacking security updates and upstream support.
- **Security:** Continued use may expose the stack to unresolved CVEs.
- **Compliance:** Dependencies must be actively maintained to meet minimum security and compliance policies.
- **Technical Debt:** Modern features introduced in 2.0.x enable more performant and maintainable code.
- **Upgrade Urgency:** Medium, as noted in the tech analysis, due to a balance of feature needs and compliance timelines.

## Current State

- **ORM Usage:** Codebase relies on SQLAlchemy 1.3 ORM interfaces.
- **Session Management:** Utilizes 1.3 session and transaction patterns.
- **Query Interface:** Relies on 1.x style query construction and execution.
- **Config/Engine:** Instantiates engines using 1.3-compatible keywords and patterns.
- **APIs/Data Models:** Classes, models, and relationships are structured according to 1.3 conventions.
- **Class/Config References:** Details TBD — explicit class names, config keys, and schema elements not provided in context.

## Proposed Changes

| Component         | Before (1.3)             | After (2.0.x)                 | Breaking? |
|-------------------|--------------------------|-------------------------------|-----------|
| ORM API           | 1.3 style ORM usage      | 2.0 style ORM usage           | Y         |
| Session Management| Legacy patterns (commit/rollback, context) | 2.0 session patterns (contextual, new semantics) | Y         |
| Query API         | 1.x style queries        | 2.0 style queries (fully 2.0 API) | Y         |
| Engine/Config     | 1.3 engine instantiation | 2.0 engine instantiation      | Y         |
| Deprecated APIs   | Many APIs/shortcuts in use| Deprecated/removed in 2.0.x   | Y         |
| Third-party Plugins| 1.3-compatible versions | 2.0.x-compatible versions     | TODO      |

## Compatibility & Breaking Changes

| Breaking Change                              | Migration Path                                  |
|----------------------------------------------|-------------------------------------------------|
| ORM API: Removed/renamed methods and patterns| Refactor code to comply with 2.0.x               |
| Session and transaction management overhauled| Adopt 2.0 session/transaction idioms             |
| Legacy query construction removed            | Migrate to 2.0 style queries                     |
| Deprecated config options dropped            | Clean up config to approved 2.0.x schema         |
| Removal of synchronous APIs where applicable | Migrate to async patterns if used                |
| Third-party SQLAlchemy plugins/integrations may break | TODO                                           |

## Acceptance Criteria

1. **Given** the application is built with SQLAlchemy 2.0.x in the environment, **when** the full test suite is executed, **then** no SQLAlchemy-related deprecation or compatibility warnings appear.
2. **Given** the upgraded codebase, **when** all main workflows using database operations are run, **then** no SQLAlchemy exceptions related to removed or changed APIs from version 1.3 are encountered.
3. **Given** a standard database schema in use with the application, **when** all migration commands (e.g., via Alembic, if used) are invoked, **then** migrations complete successfully without errors arising from the upgrade.
4. **Given** the database interface layer, **when** code linting or static analysis runs, **then** no direct usage of APIs deprecated or removed in SQLAlchemy 2.0.x are present.
5. **Given** test cases that simulate basic CRUD operations, **when** executed in CI, **then** the observed behaviour matches pre-upgrade semantics and all tests pass.

## Open Questions

| #  | Question                                                              | Owner (or TODO) | Due Date (or TODO) |
|----|-----------------------------------------------------------------------|-----------------|--------------------|
| 1  | What are the precise versions and compatibility of dependent plugins?  | TODO            | TODO               |
| 2  | Which specific classes, config keys, and data models are affected?     | TODO            | TODO               |
| 3  | Are there any indirect or transitive dependencies on SQLAlchemy APIs?  | TODO            | TODO               |
| 4  | Is Alembic or other migration tooling in use, and what versions?       | TODO            | TODO               |
| 5  | Do any runtime or language requirements restrict this upgrade?         | TODO            | TODO               |