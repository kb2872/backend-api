from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.auth import router as auth_router


app = FastAPI(
    title="HenryLab API",
    description="Mi primera API con FastAPI",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Bienvenido a RyguLab 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


app.include_router(users_router)
app.include_router(auth_router)






