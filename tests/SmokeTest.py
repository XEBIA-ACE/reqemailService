import unittest
import sqlalchemy
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

# Minimal test model setup
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

# Example of new 2.0-style config key (future_engine)
NEW_CONFIG_KEY = {"future": True}

TARGET_SQLALCHEMY_MAJOR = 2
TARGET_SQLALCHEMY_MINOR = 0  # Accept any 2.0.x version

class TestSQLAlchemyUpgrade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use in-memory SQLite for testing
        engine = create_engine("sqlite:///:memory:", **NEW_CONFIG_KEY)
        Base.metadata.create_all(engine)
        cls.engine = engine
        cls.Session = sessionmaker(bind=engine, future=True)

    def test_sqlalchemy_version(self):
        version_tup = tuple(int(x) for x in sqlalchemy.__version__.split(".")[:2])
        self.assertEqual(version_tup[0], TARGET_SQLALCHEMY_MAJOR, "SQLAlchemy major version is not 2 (upgrade incomplete)")
        self.assertEqual(version_tup[1], TARGET_SQLALCHEMY_MINOR, "SQLAlchemy minor version is not 0 (target is 2.0.x)")

    def test_orm_query_20_api(self):
        # 2.0+ style session and Select
        with self.Session() as session:
            user = User(name="Alice")
            session.add(user)
            session.commit()
            stmt = sqlalchemy.select(User).where(User.name == "Alice")
            result = session.execute(stmt)
            fetched_user = result.scalar_one()
            self.assertEqual(fetched_user.name, "Alice", "2.0 style query failed after upgrade")

    def test_deprecated_apis_gone(self):
        # Query object no longer available from session in 2.0
        with self.Session() as session:
            with self.assertRaises(AttributeError):
                # .query attribute/shortcut removed
                session.query(User)
        # Engine.execute is removed in 2.0
        with self.assertRaises(AttributeError):
            self.engine.execute(text("SELECT 1"))

    def test_new_engine_config_key_applied(self):
        # The 'future' key is required in 2.0.x for full 2.0 mode in pre-2.0 environments
        # In 2.0, it is accepted but not required; supplying it should have no effect (no errors)
        try:
            engine = create_engine("sqlite:///:memory:", future=True)
            # Try creating a simple table to ensure engine works with new config
            Base.metadata.create_all(engine)
        except Exception as e:
            self.fail(f"Engine failed to instantiate or create tables with new config key 'future': {e}")

    def test_critical_sql_path_insert_and_fetch(self):
        # Insert and fetch using the new session semantics (autobegin, commit, etc.)
        with self.Session() as session:
            user = User(name="Bob")
            session.add(user)
            session.commit()
        with self.Session() as session:
            stmt = sqlalchemy.select(User).where(User.name == "Bob")
            user_bob = session.execute(stmt).scalar_one()
            self.assertEqual(user_bob.name, "Bob", "Data fetch via critical path failed in 2.0 mode")

    def test_no_legacy_transaction_patterns(self):
        # 'autocommit' and 'autoflush' arguments deprecated/removed
        with self.assertRaises(TypeError):
            _ = sessionmaker(bind=self.engine, autocommit=True)
        with self.assertRaises(TypeError):
            _ = sessionmaker(bind=self.engine, autoflush=False)

if __name__ == "__main__":
    unittest.main()