from datetime import datetime

from pydantic import BaseModel

__all__ = (
    "UserModel",
    "UserCreate",
    "UserPatch",
    "UserListResponse",
)


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserPatch(UserBase):
    id: int


class UserModel(UserBase):
    id: int
    roles: str
    is_superuser: bool
    uuid: str
    is_totp_enabled: bool
    is_active: bool
    created_at: datetime


class UserListResponse(BaseModel):
    users: list[UserModel] = []


