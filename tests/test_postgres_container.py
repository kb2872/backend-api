from sqlalchemy import create_engine, text
from testcontainers.community.postgres import PostgresContainer


def test_postgres_container_is_real_postgres():
    with PostgresContainer("postgres:15") as postgres:
        engine = create_engine(postgres.get_connection_url())

        with engine.connect() as connection:
            version = connection.execute(
                text("SELECT version()")
            ).scalar_one()

        assert version.startswith("PostgreSQL")
