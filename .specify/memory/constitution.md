## Quality Standards / Design Principles

1. **Code compatibility**: All refactored modules must be compatible with Python 3.x, Flask 3.0, and SQLAlchemy 2.0.
2. **Backward compatibility**: Where feasible, changes should not break existing APIs or data schemas.
3. **Test coverage**: Unit and integration tests must cover all upgraded code. Maintain or improve current coverage levels.
4. **Documentation**: All upgrade-related changes and issues must be documented at the module/function level.
5. **Error handling**: Refactored code must handle all Flask/SQLAlchemy deprecations, exceptions, and breaking changes as specified by upstream documentation (SME review required).
6. **No silent failure**: If a module or class cannot be cleanly upgraded, escalate for SME or architect review immediately.
7. **Separation of concerns**: Changes should be isolated to in-scope modules unless dependency analysis confirms a wider impact.
8. **Standards alignment**: Adhere to organization’s code conventions and enforcement tools for Python.
