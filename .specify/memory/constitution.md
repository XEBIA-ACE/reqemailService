## Constitution and Standards
1. **Zero Hallucination:** All technical assertions must be documented with CAST-derived object/ID/graph citations. SME/manual notes required for anything not in the CAST snapshot.
2. **Backward Compatibility:** Test suite changes must not break any modules or workflows, unless flagged/approved for removal.
3. **Coverage Requirements:** Minimum coverage rules as set by CarePay policy apply. Newly added code must have automated test coverage.
4. **Tech/Version Alignment:** Test tools must match runtime versions detected: Angular (20.x), Cypress (14.x), Jest, Typescript, and related packages.
5. **Documentation:** Test results, coverage, and change summaries should be tracked and published for team QA.
6. **Extensibility:** Make configs/test runners easily upgradable to new major versions (future Angular/Node/Python/Java/Spring).

---

**Boundaries and Scoping:**
- GR-12/13 (batch/micro-boundaries): Not applicable for a test-suite/feature-level enhancement spec.
- GR-08: BCM scope was not provided. App-wide queries have been run and compliance gap logged in every field.

---