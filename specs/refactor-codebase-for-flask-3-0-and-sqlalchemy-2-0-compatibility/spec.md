## Refactor codebase for Flask 3.0 and SQLAlchemy 2.0 compatibility

**Source:** Requirement provided from a non-CAST document. No Business Capability Model (BCM) scoping provided; this is a standing compliance gap per GR-08.

### Objective
Refactor the CarePay application's Python codebase to ensure compatibility with Flask 3.0 and SQLAlchemy 2.0.

### Scope
- Python modules and classes discovered in CarePay matching "model", "db", and migration patterns (e.g., "alembic") are in scope.
- Any code currently leveraging Flask or SQLAlchemy, or performing database interaction through Python (or ORM models) is in scope.
- Java components, REST endpoints, and other technologies are out of scope for this upgrade (GR-11, GR-16).

### Requirements
1. Identify all Python modules, methods, and classes that define, reference, or interact with database models and configurations.
2. Identify SQL interaction layers (e.g., modules named "db", "models").
3. Refactor these Python files to ensure compatibility with Flask 3.0 and SQLAlchemy 2.0. The exact changes will be defined by technology upgrade documentation (⚠️ SME validation required — not available in CAST MCP).
4. Migration-related modules (e.g., "alembic") and any code that integrates with ORM models or the Flask app factory pattern are included if present.
5. All other application layers remain in their current versions unless evidence surfaces that Flask/SQLAlchemy interoperation is present.

### Compliance
- Absence of BCM component scope is a standing compliance gap. All findings are application-wide.
- All name/ID pairs, table names, and code facts are in the Technical Appendix—none in this body.
- This specification excludes any granular technology upgrade guidance, which is subject to validation and must be sourced from Flask/SQLAlchemy official changelogs (GR-02).

### Limitations
- CAST MCP queries for explicit "flask" and "sqlalchemy" objects returned no matches (❌).
- Python modules matching "model" and "db" exist and are included in the actionable scope (✅).

### Out of Scope
- Java modules, classes, and services (not Python-based, not Flask/SQLAlchemy driven).
- Any architectural decomposition or migration plans that depend on code function rather than existence/name per CAST.
