from pydantic import BaseModel, EmailStr,Field
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    phone_no: str
    password: str=Field(
        min_length=8,
        max_length=64
    )

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class TokenRequest(BaseModel):
    token:str