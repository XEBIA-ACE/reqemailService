# CONSTITUTION: SQLAlchemy 1.3 → 2.0.x Modernization

## Project Identity

**Name**: SQLAlchemy Major Version Upgrade

**Purpose**:  
Migrate the project's use of SQLAlchemy from version 1.3 to the latest 2.0.x release series.

**High-Level Goal**:  
Eliminate dependencies on SQLAlchemy 1.3, enabling maintenance and feature development on code that interoperates safely and fully with SQLAlchemy 2.0.x.

---

## Guiding Principles

1. **Prefer code changes that achieve SQLAlchemy 2.0.x compatibility over retaining deprecated 1.3 patterns, because 1.3 is EOL and may introduce security or stability risks.**
2. **Prefer automated refactoring tools and test-backed changes over manual code edits, because this minimizes regression risk during major upgrades.**
3. **Prefer minimal, targeted modifications over broad rewrites, because upgrade urgency is medium and tech debt specifics are not provided.**
4. **Prefer explicitly resolving all 2.0.x-breaking changes documented by SQLAlchemy, because silent incompatibilities may cause runtime failures.**

---

## Constraints

- **Timeline and Effort Ceiling**:  
  *Must not exceed the person-days estimate defined in upgrade option 'moderate'.*  
  (Actual numbers: **TODO** — upgrade option details not provided.)

- **Technology Mandates**:  
  - *Target SQLAlchemy 2.0.x as runtime dependency.*  
  - *No other language, runtime, or build tool requirements surfaced.*  
  - *Compliance requirements: N/A — not applicable to this task.*

- **Budget or Scope Freezes**:  
  - *Scope is limited to upgrading SQLAlchemy from 1.3 to 2.0.x. No additional features or unrelated refactoring is permitted.*

---

## Quality Standards

- **Test Coverage**:  
  - *All lines of code affected by the upgrade must be covered by automated tests (unit or integration).*  
  - *No upgrade PR may merge with reduced existing test coverage.*

- **Code Review**:  
  - *Every change must pass at least one reviewer with context on SQLAlchemy migration.*

- **Documentation**:  
  - *Changelog entry must concisely summarize all user-facing and developer-facing upgrade impacts (minimally: new minimum SQLAlchemy version, key migrated APIs).*  

- **Deployment Gates**:  
  - *All CI tests must pass in an environment using SQLAlchemy 2.0.x before upgrade code can be merged to main.*

---

## Decision Log

| ID   | Decision                                                   | Rationale                                          | Status   |
|------|------------------------------------------------------------|----------------------------------------------------|----------|
| ADR1 | Upgrade SQLAlchemy from 1.3 to 2.0.x in a single cycle     | Upgrade urgency is medium; no gradual bridge pattern required | Accepted |
| ADR2 | Disallow deprecated 1.3 APIs post-upgrade                  | EOL risk; prevents silent breakage in future         | Accepted |
| ADR3 | Scope limited strictly to SQLAlchemy version migration     | Budget/scope constraints from upgrade option         | Accepted |
| ADR4 | Require passing tests on SQLAlchemy 2.0.x before merge     | Ensures zero-regression on supported runtime         | Accepted |
| ADR5 | Testing and review required for all upgrade-related changes| Minimizes risk of undetected breaking changes        | Accepted |

---

*Sections not directly applicable to this task have been omitted per instructions.*