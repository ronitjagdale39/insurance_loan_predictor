from fastapi import APIRouter,HTTPException
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken
from app.db.database import get_db
from app.core.security import hashed_refresh_token
from app.routers.refresh import RefreshTokenRequest
router=APIRouter(prefix="/auth",tags=["auth"])
@router.post('/logout')
def logout(token:RefreshTokenRequest,db:Session=Depends(get_db)):
    try:
        refresh_token=token.refresh_token
        hashed_rt=hashed_refresh_token(refresh_token)
        db_rt=db.query(RefreshToken).filter(RefreshToken.token_hash==hashed_rt).first()
        if db_rt is not None:
            db.delete(db_rt)
            db.commit()
            return {
                "detail":"user logout successful"
            }
        else:
            raise HTTPException(status_code=404,detail="token not found")
    except HTTPException:
        raise
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500,detail="server error")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500,detail="Unexpected error occured")
    