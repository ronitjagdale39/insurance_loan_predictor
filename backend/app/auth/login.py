from fastapi import status
from app.schemas.auth import LoginRequest,SignupRequest
from app.models.user import User
from app.models.user_token import UserToken
from app.db.database import get_db
from app.core.security import verify_password,create_access_token,hashed_password,create_refresh_token,hashed_refresh_token,generate_secure_token
from jose import jwt,JWTError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from app.models.refresh_token import RefreshToken
from datetime import datetime, timedelta
from app.core.config import settings
from app.services.email_verify import sent_verification_email
Oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth",tags=["auth"])
@router.post("/check")
def status():
    return {
        "message":"API is running",
        "version":"1.0"
    }
@router.post("/signup")
def signup(user:SignupRequest,db:Session=Depends(get_db)):
    db_existing_user=db.query(User).filter(User.email==user.email).first()
    if db_existing_user:
        raise HTTPException(status_code=400,detail="user already exists")
    new_user=User(
        name=user.name,
        email=user.email,
        phone_no=user.phone_no,
        hashed_password=hashed_password(user.password)
    )  

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # after adding the user we will be sending email verification to the user ...
    # here we are generating secure token for email verification
    token=generate_secure_token()
    hash_token=hashed_refresh_token(token)
    db_token=UserToken(
        user_id=new_user.id,
        token_hash=hash_token,
        token_type="email_verification",
        expires_at=datetime.utcnow()+timedelta(minutes=settings.VERIFICATION_TOKEN_EXPIRE_MINUTES)
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    sent_verification_email(new_user.email,token)
    
    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "message": "User created successfully"
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    username = form_data.username
    password = form_data.password

    db_user = db.query(User).filter(
        User.name == username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    access_token = create_access_token(
        {
            "sub": str(db_user.id),
            "email": db_user.email,
            "role": db_user.role
        }
    )
    refresh_token=create_refresh_token(
            {"sub": str(db_user.id),
            "email": db_user.email}
    )
    hashed_rt=hashed_refresh_token(refresh_token)
    db_rt=RefreshToken(
        user_id=db_user.id,
        token_hash=hashed_rt,
        expires_at=datetime.utcnow()+timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    )
    db.add(db_rt)
    db.commit()
    db.refresh(db_rt)

    return {
        "userrole":db_user.role,
        "access_token": access_token,
        "refresh_token":refresh_token,
        "token_type": "bearer",
        "must_change_password":db_user.is_first_login
    }