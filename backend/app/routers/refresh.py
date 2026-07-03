from requests import Session
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt ,JWTError
from app.core.security import create_access_token,create_refresh_token
from app.core.config import settings
from app.models.user import User
from app.db.database import get_db
router=APIRouter()
class RefreshTokenRequest(BaseModel):
    refresh_token: str
@router.post('/refresh')
def refresh(request:RefreshTokenRequest,db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(
            request.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_type=payload.get('type')
        if token_type!='refresh_token':
            raise HTTPException(status_code=401,detail="Invalid token type")
        user_id=payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=401,detail="User not found")
        user=db.query(User).filter(User.id==int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401,detail="Invalid details")
        new_access_token=create_access_token({"sub":str(user.id),"email":user.email,"role":user.role})
        return {
            "access_token":new_access_token
        }
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")
