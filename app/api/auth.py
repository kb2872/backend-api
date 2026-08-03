from fastapi import APIRouter

from app.schemas.auth import LoginRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(data: LoginRequest):
    return {
        "email": data.email,
        "message": "Datos recibidos correctamente"
    }




