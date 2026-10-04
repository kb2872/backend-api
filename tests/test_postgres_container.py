from sqlalchemy import text


def test_postgres_container_is_real_postgres(db_engine):
    with db_engine.connect() as connection:
        version = connection.execute(
            text("SELECT version()")
        ).scalar_one()

    assert version.startswith("PostgreSQL")
