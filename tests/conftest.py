import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from testcontainers.community.postgres import PostgresContainer

from app.core.roles import Role
from app.core.security import hash_password
from app.db.database import Base, get_db
from app.main import app
from app.models.user import User


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def db_engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    Base.metadata.create_all(bind=db_engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine,
    )

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=db_engine)


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
