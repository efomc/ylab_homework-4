from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from src.api.v1.schemas import UserCreate, UserModel
from src.services import UserService, get_user_service

router = APIRouter()


@router.post(
    path="/",
    response_model=UserModel,
    summary="Зарегистрировать пользователя",
    tags=["users"],
)
def user_create(
    user: UserCreate, user_service: UserService = Depends(get_user_service),
) -> UserModel:
    user_check: Optional[dict] = user_service.check_user_name(username=user.username)
    if user_check:
        # Если пользователь с таким именем существует, отдаём 406 статус
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail="username exists")
    new_user: dict = user_service.create_user(user=user)
    return UserModel(**new_user)


