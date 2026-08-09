from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.services.user_service import get_user_by_id



security = HTTPBearer()



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("sub")


    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )


    user = get_user_by_id(db, int(user_id))
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )
    return user


















