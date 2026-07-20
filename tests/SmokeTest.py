import sys
import importlib
import re

import pytest

# These constants define the exact target versions after the upgrade
TARGET_FLASK_VERSION = "3.0"
TARGET_SQLALCHEMY_VERSION = "2.0"

@pytest.fixture(scope="module")
def flask_module():
    return importlib.import_module("flask")

@pytest.fixture(scope="module")
def sqlalchemy_module():
    return importlib.import_module("sqlalchemy")

def normalize_version(version_string):
    """
    Convert a version string to MAJOR.MINOR for comparison.
    """
    match = re.match(r"^(\d+\.\d+)", version_string)
    if match:
        return match.group(1)
    return version_string

def test_flask_version_is_3_0(flask_module):
    version = getattr(flask_module, "__version__", None)
    assert version is not None, "Flask module does not have __version__"
    assert normalize_version(version) == TARGET_FLASK_VERSION, f"Expected Flask {TARGET_FLASK_VERSION}, found {version}"

def test_sqlalchemy_version_is_2_0(sqlalchemy_module):
    version = getattr(sqlalchemy_module, "__version__", None)
    assert version is not None, "SQLAlchemy module does not have __version__"
    assert normalize_version(version) == TARGET_SQLALCHEMY_VERSION, f"Expected SQLAlchemy {TARGET_SQLALCHEMY_VERSION}, found {version}"

def test_critical_flask_app_path_import_and_run():
    """
    Verify that the Flask app can be created and a simple view works under Flask 3.0 and SQLAlchemy 2.0.
    """
    from flask import Flask
    import sqlalchemy

    app = Flask(__name__)
    @app.route("/healthz")
    def healthz():
        return "ok"

    # Use the Flask test client to simulate a request
    with app.test_client() as client:
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.data == b"ok"

def test_sqlalchemy_session_creation_and_model_crud(tmp_path):
    """
    Verify that a simple SQLAlchemy model can be defined and used with correct session semantics,
    using SQLAlchemy 2.0 style (no deprecated APIs).
    """
    import sqlalchemy as sa
    from sqlalchemy.orm import DeclarativeBase, Session

    class Base(DeclarativeBase):
        pass

    class Item(Base):
        __tablename__ = "items"
        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.String, nullable=False)

    engine = sa.create_engine(f"sqlite:///{tmp_path}/test.db", echo=False, future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        item = Item(name="test")
        session.add(item)
        session.commit()

        retrieved = session.get(Item, item.id)
        assert retrieved is not None
        assert retrieved.name == "test"

def test_no_deprecated_sqlalchemy_apis():
    """
    Confirm that deprecated SQLAlchemy 1.x APIs no longer exist or fail as expected.
    For example, Session.query_property was removed in 2.0.
    """
    import sqlalchemy.orm

    # Session.query_property was deprecated and removed in 2.0
    assert not hasattr(sqlalchemy.orm.Session, 'query_property'), "Session.query_property should not exist in SQLAlchemy 2.0"

def test_sqlalchemy_new_config_key_future_flag():
    """
    Newer SQLAlchemy 2.0 configurations use particular flags; test that no error occurs on 'future=True'.
    """
    import sqlalchemy

    # The 'future=True' parameter should be accepted
    engine = sqlalchemy.create_engine("sqlite:///:memory:", future=True)
    # Check engine object exists and works
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT 1"))
        assert result.scalar() == 1

def test_flask_configure_cli_loader():
    """
    Flask 3.0 introduces CLI-related configuration keys (for instance, 'ENV' is removed, 'FLASK_DEBUG' recommended).
    Verifies new keys do not error out.
    """
    from flask import Flask

    app = Flask(__name__)
    app.config["FLASK_DEBUG"] = True
    # 'ENV' config removed in Flask 3.0, check access fails cleanly
    with pytest.raises(KeyError):
        _ = app.config["ENV"]
    # FLASK_DEBUG set above should work
    assert app.config["FLASK_DEBUG"] is True