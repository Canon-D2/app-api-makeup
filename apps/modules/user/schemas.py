from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr, Field, validator
from apps.utils.validator import Validator

class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    phone: str  
    password: str
    permission: Literal["member"] = "member"
    gender: Literal["male", "female", "other"]
    birthday: float
    avatar: Optional[str] = None
    address: str

    @validator("phone")
    def check_phone(cls, v):
        if not Validator.is_vietnamese_phone(v):
            raise ValueError("Phone number consists of 10 digits, starting with 0 or +84")
        return v

    @validator("password")
    def check_password(cls, v):
        if not Validator.is_password_valid(v):
            raise ValueError("Password must be 8-12 characters, at least 1 uppercase letter, 1 number and 1 special character")
        return v

class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    password: Optional[str] = None
    permission: Optional[Literal["admin", "artist", "member"]] = None
    gender: Optional[Literal["male", "female", "other"]] = None
    birthday: Optional[float] = None
    avatar: Optional[str] = None
    phone: Optional[str] = None  
    address: Optional[str] = None


class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    fullname: Optional[str]
    email: EmailStr
    # password: Optional[str]
    permission: Optional[str]
    gender: Optional[str]
    birthday: Optional[float]
    avatar: Optional[str] = None
    phone: Optional[str]
    address: Optional[str]


class PaginatedUserResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[UserResponse]
