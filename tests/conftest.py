import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password
from app.core.roles import Role
from app.db.database import Base, get_db
from app.main import app
from app.models.user import User


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def create_user(
    db_session,
    *,
    name="Test User",
    email="user@example.com",
    password="secret123",
    role=Role.CUSTOMER.value,
    with_password=True,
):
    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password) if with_password else None,
        role=role,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def superadmin(db_session):
    return create_user(
        db_session,
        name="Root",
        email="root@example.com",
        password="rootpass",
        role=Role.SUPERADMIN.value,
    )


@pytest.fixture
def customer(db_session):
    return create_user(
        db_session,
        name="Customer",
        email="customer@example.com",
        password="custpass",
        role=Role.CUSTOMER.value,
    )


def auth_headers(client, email, password):
    response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
