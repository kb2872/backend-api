from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.db.database import get_db
from app.schemas.auth import LoginRequest
from app.services.user_service import get_user_by_email


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)



    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )


    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )


    token = create_access_token(
         data={"sub": str(user.id)}
     )


    return {
        "access_token": token,
        "token_type": "bearer"
    }



