from fastapi import Depends,APIRouter,HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from datetime import datetime
from app.models.user_token import UserToken
from app.models.user import User
from app.core.security import hashed_refresh_token,hashed_password
from app.schemas.auth import ResetPassword

router=APIRouter(prefix="/auth",tags=["auth"])
@router.post("/reset-password")
def reset_password(user:ResetPassword,db:Session=Depends(get_db)):
    try:
        hash_token=hashed_refresh_token(user.token)
        db_user=(db.query(UserToken).filter(
            UserToken.token_hash==hash_token,
            UserToken.token_type=='reset_password',
            UserToken.used==False  
            ).first())
        if not db_user:
            raise HTTPException(status_code=404,detail="invalid token")
        if db_user.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=400,
                detail="Token has expired."
            )
        db_token_user=db.query(User).filter(User.id==db_user.user_id).first()
        if not db_token_user:
            raise HTTPException(
    status_code=400,
    detail="Invalid or expired token."
)
        new_hash=hashed_password(user.new_password)
        db_token_user.hashed_password=new_hash
        db_user.used=True
        db.commit()
        db.refresh(db_user)
        return {
            'message':'password reset successfully'
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

    