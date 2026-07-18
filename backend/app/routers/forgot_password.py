from fastapi import Depends,APIRouter,HTTPException
from fastapi import Request
from app.services.audit_log import AuditService
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from app.core.config import settings
from app.services.email_verify import send_password_reset_email
from app.db.database import get_db
from app.core.security import generate_secure_token,hashed_refresh_token
from app.schemas.auth import ForgotPassword
from app.models.user_token import UserToken
from app.models.user import User
router=APIRouter(prefix="/auth",tags=["auth"])
@router.post("/forgot-password")
def forgot_password(request:Request,user:ForgotPassword,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()
    if not db_user:
        AuditService.log(
            db=db,
            event="RESET_PASSWORD",
    level="WARNING",
    user_id=None,
    email=None,
    endpoint=request.url.path,
    method=request.method,
    status_code=401,
    ip_address=request.client.host if request.client else None,
    message="User doesnt exists",
    payload={
        "reason":"User doesnt exists",
        "signup_type":"email",
    }
    )
    return {
        "message": "If an account exists, a password reset link has been sent."
        }
    if not db_user.is_verified:
        AuditService.log(
        db=db,
        event="RESET_PASSWORD",
        level="WARNING",
        user_id=db_user.id,
        email=db_user.email,
        endpoint=request.url.path,
        method=request.method,
        status_code=403,
        ip_address=request.client.host if request.client else None,
        message="Password reset attempted on unverified account",
        payload={}
    )
        return {
        "message": "If an account exists, a password reset link has been sent."
        }
    old_tokens=(db.query(UserToken).filter(UserToken.user_id==db_user.id,UserToken.token_type=='reset_password',UserToken.used==False).all())
    for token in old_tokens:
        token.used=True
    db.commit()
    # now we will be generating new token 
    new_token=generate_secure_token()
    hash_token=hashed_refresh_token(new_token)
    db_new=UserToken(
        user_id=db_user.id,
        token_hash=hash_token,
        token_type='reset_password',
        used=False,

        created_at=datetime.utcnow(),

        expires_at=datetime.utcnow() + timedelta(

            minutes=settings.RESET_PASSWORD_TOKEN_EXPIRE_MINUTES

    )
    )
    db.add(db_new)
    db.commit()
    db.refresh(db_new)
    # now we will be sending email verification to the user 
    send_password_reset_email(db_user.email,new_token)
    AuditService.log(
            db=db,
            event="RESET_PASSWORD",
    level="SUCCESS",
    user_id=db_user.id,
    email=db_user.email,
    endpoint=request.url.path,
    method=request.method,
    status_code=200,
    ip_address=request.client.host if request.client else None,
    message="Password reset link sent successfully",
    payload={
        "Link send":True
    }
        )
    return {
        'message':'if your acoount exists then u will recieve a mail to reset your password'
    }
    
