from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.core.security import verify_password, hashed_password

from app.auth.dependencies import get_current_user  

router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/change-password")
def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):


    if not verify_password(old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid old password"
        )


    current_user.hashed_password = hashed_password(new_password)


    current_user.is_first_login = False

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Password changed successfully",
        "status": "success"
    }

        
