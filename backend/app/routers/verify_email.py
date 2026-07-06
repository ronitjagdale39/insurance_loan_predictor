from fastapi import APIRouter,HTTPException
from fastapi import Depends
from app.db.database import get_db
from app.schemas.auth import TokenRequest
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user_token import UserToken
from app.core.security import hashed_refresh_token
router=APIRouter(prefix="/auth")
@router.get('/verify_email')
def verify_email(token:str,db:Session=Depends(get_db)):
    hashed_token=hashed_refresh_token(token)
    db_verify=db.query(UserToken).filter(UserToken.token_hash==hashed_token,UserToken.token_type=="email_verification",UserToken.expires_at>datetime.utcnow(),UserToken.used==False).first()
    if not db_verify:
        raise HTTPException(status_code=400,detail="invalid or expired verification token")
    db_verify.used=True
    db_verify.user.is_verified=True
    db.commit()
    return {
    "message": "Email verified successfully",
    "verified": True
    }