

from pydantic import BaseModel,EmailStr
class UserCreate(BaseModel):
    name:str
    email:EmailStr
    phone_no:str


class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    phone_no:str

    class Config:
        from_attributes=True
    