## Task List

1. **Review and inventory all test configs and scripts**
   - Include all objects/files found matching jest, cypress, test, mock, e2e (see Appendix of objects:name queries 16–31 below).
   - SME/manual code inspection to confirm Java, Python, or Spring test sources absent in CAST results.

2. **Update and validate config files:**
   - Examine and validate `jest.config.ts`, `cypress.config.ts`, `*.jest.mock.ts`, and other JS/TS test configs for compatibility with new package versions.
   - Retire obsolete or duplicate configs, if any, and consolidate setup as needed for monorepo or module boundaries.

3. **Assess frontend coverage:**
   - Cross-check detected test/spec/mocks/e2e.ts files with each UI/feature module.
   - Confirm presence/absence of `.spec.ts` (none found in CAST), propose SME/manual check for hidden/unconventional test files.

4. **Assess backend coverage:**
   - Validate that server-side tests (Java, Spring, Python) are present or provide a gap list if missing (none discovered in CAST for these languages).

5. **Audit and upgrade dependencies**
   - Compare package.json/yarn.lock/requirements.txt/Gradle against newly supported versions (Angular 20+, Cypress 14+, etc, see package list).
   - Propose upgrades and update dependency scripts accordingly.

6. **Extend and run expanded test suite**
   - Implement missing scripts; upgrade and refactor test runners for each framework/package/target runtime.
   - Run full test suite and prepare validation evidence for stakeholders.

---