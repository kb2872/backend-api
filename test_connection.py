from sqlalchemy import text

from app.db.database import engine

try:
    with engine.connect() as connection:
        version = connection.execute(text("SELECT version();"))

        print("\n✅ Conexión exitosa\n")

        for row in version:
            print(row[0])

except Exception as e:
    print("\n❌ Error de conexión:\n")
    print(e)



