from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt,JWTError
from app.models.user import User
from app.db.database import get_db
from app.core.security import settings
Oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token:str=Depends(Oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401,detail="token invalid")
        user=db.query(User).filter(User.id==int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401,detail="Invalid Authetication Credentials ....")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
def role_required(allowed_roles: list):
    def wrapper(current_user:User=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )
        return current_user
    return wrapper