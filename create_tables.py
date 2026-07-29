from app.db.database import Base, engine

# Importa los modelos para que SQLAlchemy los conozca
from app.models.user import User

print("Creando tablas...")

Base.metadata.create_all(bind=engine)

print("Listo.")



