from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.dependencies import require_admin
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import (
    get_users,
    create_user,
    get_user_by_id,
    delete_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin),
):
    return get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin),
):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user



@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    responses={
        409: {
            "description": "El correo ya está registrado"
        }
    }
)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.delete("/{user_id}", status_code=204)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return



from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)

from app.services.user_service import (
    get_users,
    get_user_by_id,
    create_user,
    delete_user,
    update_user,
)


@router.put("/{user_id}", response_model=UserResponse)
def edit_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    updated = update_user(db, user_id, user)

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return updated



