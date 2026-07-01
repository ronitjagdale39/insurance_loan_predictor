from fastapi import status
from app.schemas.auth import LoginRequest,SignupRequest
from app.models.user import User
from app.db.database import get_db
from app.core.security import verify_password,create_access_token,hashed_password
from jose import jwt,JWTError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
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
    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "message": "User created successfully"
    }

@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        user.password,
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

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
