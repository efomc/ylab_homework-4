import json
from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlmodel import Session

from src.api.v1.schemas import UserCreate, UserModel, UserPatch
from src.db import AbstractCache, get_cache, get_session
from src.models import User
from src.services import ServiceMixin

__all__ = ("UserService", "get_user_service")


class UserService(ServiceMixin):
    def get_user_list(self) -> dict:
        """Получить список пользователей."""
        users = self.session.query(User).order_by(User.created_at).all()
        return {"users": [UserModel(**user.dict()) for user in users]}

    def get_user_detail(self, item_id: int) -> Optional[dict]:
        """Получить детальную информацию о пользователе."""
        if cached_user := self.cache.get(key=f"{item_id}"):
            return json.loads(cached_user)

        user = self.session.query(User).filter(User.id == item_id).first()
        if user:
            self.cache.set(key=f"{user.id}", value=user.json())
        return user.dict() if user else None

    def check_user_name(self, username: str) -> Optional[int]:
        """Проверить пользователя с данным именем."""
        if cached_user := self.cache.get(key=f"{username}"):
            return UserModel(**json.loads(cached_user)).id

        user = self.session.query(User).filter(User.username == username).first()
        if user:
            self.cache.set(key=f"{user.username}", value=user.json())
        return user.id if user else None

    def create_user(self, user: UserCreate) -> dict:
        """Создать пользователя."""
        new_user = User(username=user.username, email=user.email, password=user.password)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user.dict()

    def update_user_detail(self, user: UserPatch):
        patch_user = self.session.query(User).filter(User.id == user.id).first()
        patch_user.username = user.username
        patch_user.email = user.email
        self.session.add(patch_user)
        self.session.commit()
        self.session.refresh(patch_user)
        return patch_user.dict()


# get_user_service — это провайдер UserService. Синглтон
@lru_cache()
def get_user_service(
    cache: AbstractCache = Depends(get_cache),
    session: Session = Depends(get_session),
) -> UserService:
    return UserService(cache=cache, session=session)
