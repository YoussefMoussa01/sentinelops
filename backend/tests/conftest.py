"""Shared isolated API test fixtures."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database.session import Base, get_db
from app.main import app
from app.models import User
from app.core.security import create_access_token


@pytest.fixture()
def api_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with session_factory() as db:
        admin = User(
            username="test-admin",
            email="test-admin@example.com",
            password_hash="unused-test-hash",
            role="SOC_ADMIN",
        )
        viewer = User(
            username="test-viewer",
            email="test-viewer@example.com",
            password_hash="unused-test-hash",
            role="VIEWER",
        )
        db.add_all([admin, viewer])
        db.commit()
        db.refresh(admin)
        db.refresh(viewer)
        tokens = {
            "admin": create_access_token({"sub": admin.id}),
            "viewer": create_access_token({"sub": viewer.id}),
        }

    with TestClient(app) as client:
        client.headers.update({"Authorization": f"Bearer {tokens['admin']}"})
        yield client, tokens

    app.dependency_overrides.clear()
    engine.dispose()