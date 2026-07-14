## Implementation Plan

1. **Enumerate Python code dependencies:** Examine the Python modules and classes surfaced from CAST queries on "model" and "db" to build an in-scope target list.
    - ✅ src/models.py (96436)
    - ✅ claims-assessment/app/db/models.py (96617)
    - ✅ All referenced "db" and "model" Python classes and methods listed in the Appendix.
2. **Perform a static code audit for Flask/sqlalchemy usage:** Although explicit usage was not discoverable via object names, all database/model modules should be reviewed manually for Flask and SQLAlchemy dependencies or patterns.
    - ⚠️ SME validation required for precise Flask/SQLAlchemy upgrade requirements (out of scope for CAST MCP).
3. **Refactor all discovered model/db modules for Flask 3.0/SQLAlchemy 2.0:** Restructure imports, model declarations, configuration routines, and database operation patterns per new versions' requirements (as confirmed by SME).
4. **Validate changes:** For every refactored module, run targeted tests or static analysis to confirm compatibility.
5. **Document module changes and regression risks:** Capture modifications, note areas requiring specialized manual review, and escalate any technology upgrade issues unresolved by automated checks.

**Standing compliance gap:**
- No BCM scoping provided — entire application queried and flagged as gap per GR-08.
