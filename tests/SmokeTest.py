import sys
import importlib
import os
import pytest

TARGET_PYTHON_VERSION = (3, 12, 3)

def test_python_version():
    """
    Verify that the Python interpreter is at the exact upgraded target version.
    """
    assert sys.version_info[:3] == TARGET_PYTHON_VERSION, (
        f"Python runtime version mismatch: expected {TARGET_PYTHON_VERSION}, "
        f"but got {sys.version_info[:3]}"
    )

def test_critical_application_paths():
    """
    Verify that core Python features and common critical code paths work on Python 3.12.
    Should be customized to cover top-level app entry points if any.
    """
    # Example check: Import a core module and perform a basic operation.
    import json
    test_dict = {"foo": 1, "bar": 2}
    encoded = json.dumps(test_dict)
    decoded = json.loads(encoded)
    assert decoded == test_dict

def test_deprecated_stdlib_apis_removed():
    """
    Verify that standard library APIs removed or deprecated in Python 3.12 are not present.
    For example, collections.MutableMapping has been removed from `collections`.
    """
    import collections
    # In Python 3.12, MutableMapping, MutableSequence, etc. are no longer in collections.
    with pytest.raises(AttributeError):
        _ = collections.MutableMapping
    with pytest.raises(AttributeError):
        _ = collections.MutableSequence
    with pytest.raises(AttributeError):
        _ = collections.MutableSet

def test_stdlibrary_apireplacements_work():
    """
    Verify that new recommended APIs (e.g., from `collections.abc`) work as replacements.
    """
    from collections.abc import MutableMapping, MutableSequence, MutableSet
    assert MutableMapping is not None
    assert MutableSequence is not None
    assert MutableSet is not None

def test_new_config_keys():
    """
    Verify that configuration keys referencing Python 3.12-specific values load without error.
    This test assumes presence of at least one config file as in many projects
    (e.g., pyproject.toml, runtime.txt, .python-version), and parses their contents.
    """
    config_checks = [
        # (filename, expectation substring)
        ("pyproject.toml", ">=3.12"),
        (".python-version", "3.12.3"),
        ("runtime.txt", "python-3.12.3")
    ]
    for filename, required in config_checks:
        if os.path.exists(filename):
            with open(filename, encoding="utf-8") as f:
                content = f.read()
            assert required in content, f"{filename} does not reference upgraded Python version: {required}"

def test_import_typing_reexported_symbols():
    """
    Check that PEP 604, PEP 585 features (available in 3.9+) are available and recommended deprecated features aren't.
    E.g., using list[int] instead of List.
    """
    # list[int] is legal in Python 3.12
    l: list[int] = [1, 2, 3]
    assert isinstance(l, list)
    # typing.List exists for backward compat, but is discouraged.
    try:
        from typing import List
    except ImportError:
        pytest.skip("typing.List not present as expected in recent Python versions.")

def test_print_syntax():
    """
    Verify that the print function syntax is as expected in Python 3.12 (was unchanged since 3.x, but a trivial code path).
    """
    try:
        out = eval('print("hello world")')
        assert out is None  # print() returns None
    except SyntaxError:
        pytest.fail("print() syntax failed; unexpected for Python 3.12.")

# END OF UPGRADE VALIDATION TESTS