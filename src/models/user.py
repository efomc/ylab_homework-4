from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

__all__ = ("User",)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(default=None, nullable=False)
    email: str = Field(default=None, nullable=False)
    password: str = Field(default=None, nullable=False)
    roles: str = Field(default='[]')
    is_superuser: bool = Field(default=False, nullable=False)
    uuid: str = Field(default='')
    is_totp_enabled: bool = Field(default=False, nullable=False)
    is_active: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)