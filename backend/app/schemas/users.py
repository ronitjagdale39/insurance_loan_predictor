

from pydantic import BaseModel,EmailStr
from enum import Enum
class Role(str,Enum):
    admin="admin"
    agent="agent"
    customer="customer"

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    phone_no:str
    password:str
    role:Role=Role.customer


class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    phone_no:str
    role:Role
    class Config:
        from_attributes=True