from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User
from fastapi import Request
from app.services.audit_log import AuditService

from app.core.security import verify_password, hashed_password

from app.auth.dependencies import get_current_user  

router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/change-password")
def change_password(
    request:Request,
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):


    if not verify_password(old_password, current_user.hashed_password):
        AuditService.log(
            db=db,
            event="CHANGE_PASSWORD",
    level="WARNING",
    user_id=current_user.id,
    email=current_user.email,
    endpoint=request.url.path,
    method=request.method,
    status_code=401,
    ip_address=request.client.host if request.client else None,
    message="Invalid old password",
    payload={
        "reason":"Invalid or old password is incorrect"
    }
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid old password"
        )



    current_user.hashed_password = hashed_password(new_password)


    current_user.is_first_login = False

    db.commit()
    db.refresh(current_user)
    AuditService.log(
            db=db,
            event="PASSWORD_CHANGED",
    level="SUCCESS",
    user_id=current_user.id,
    email=current_user.email,
    endpoint=request.url.path,
    method=request.method,
    status_code=200,
    ip_address=request.client.host if request.client else None,
    message="Password changed successfully",
    payload={
        "Password Chnged":True
    }
        )
    return {
        "message": "Password changed successfully",
        "status": "success"
    }

        
