from fastapi import status
from app.schemas.auth import LoginRequest,SignupRequest
from fastapi import Request
from app.services.audit_log import AuditService
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
from app.services.email_verify import send_verification_email
Oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth",tags=["auth"])
@router.post("/check")
def status():
    return {
        "message":"API is running",
        "version":"1.0"
    }
@router.post("/signup")
def signup(request:Request,user:SignupRequest,db:Session=Depends(get_db)):
    db_existing_user=db.query(User).filter(User.email==user.email).first()
    if db_existing_user:
        AuditService.log(
    db=db,
    event="USER_SIGN_UP",
    level="WARNING",
    user_id=None,
    email=db_existing_user.email,
    endpoint="/auth/signup",
    method="POST",
    status_code=400,
    ip_address=request.client.host if request.client else None,
    message="user already exists",
    payload={
        "reason":"email_id already exits",
        'signup_type':'email',
    }
)
        raise HTTPException(status_code=400,detail="email_id  already exists")
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
    send_verification_email(new_user.email,token)
    AuditService.log(
    db=db,
    event="USER_SIGN_UP",
    level="INFO",
    user_id=new_user.id,
    email=new_user.email,
    endpoint=request.url.path,
    method=request.method,
    status_code=200,
    ip_address=request.client.host if request.client else None,
    message="User created successfully",
    payload={
        'username':user.name,
        "role": new_user.role
    }
)
    
    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "message": "User created successfully"
    }

@router.post("/login")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    username = form_data.username
    password = form_data.password

    db_user = db.query(User).filter(
        User.name == username
    ).first()

    if not db_user:
        AuditService.log(
            db=db,
            event="USER_LOGIN",
            level="WARNING",
            user_id=None,
            email=username,
            endpoint=request.url.path,
            method=request.method,
            status_code=404,
            ip_address=request.client.host if request.client else None,
            message="User not found",
            payload={
                'reason':'User not found',
                'login_type':'username'
            }
        )
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        password,
        db_user.hashed_password
    ):
        AuditService.log(
            db=db,
            event="USER_LOGIN",
            level="WARNING",
            user_id=db_user.id,
            email=db_user.email,
            endpoint=request.url.path,
            method=request.method,
            status_code=401,
            ip_address=request.client.host if request.client else None,
            message="Invalid credentials",
            payload={
                'reason':'Invalid Credentials',
                'login_type':'password'
            }
        )
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
    
    AuditService.log(
    db=db,
    event="USER_LOGIN",
    level="INFO",
    user_id=db_user.id,
    email=db_user.email,
    endpoint=request.url.path,
    method=request.method,
    status_code=200,
    ip_address=request.client.host if request.client else None,
    message="User logged in successfully",
    payload={
        "role": db_user.role
    }
)

    return {
        "userrole":db_user.role,
        "access_token": access_token,
        "refresh_token":refresh_token,
        "token_type": "bearer",
        "must_change_password":db_user.is_first_login
    }