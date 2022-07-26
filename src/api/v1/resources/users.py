from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.schemas import UserListResponse, UserModel, UserPatch
from src.services import UserService, get_user_service

router = APIRouter()


@router.get(
    path="/",
    response_model=UserListResponse,
    summary="Список пользователей",
    tags=["users"],
)
def user_list(
    user_service: UserService = Depends(get_user_service),
) -> UserListResponse:
    users: dict = user_service.get_user_list()
    if not users:
        # Если пользователи не найдены, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="users not found")
    return UserListResponse(**users)


@router.get(
    path="/me",
    response_model=UserModel,
    summary="Получить данные определенного пользователя",
    tags=["users"],
)
def user_detail(
    user_id: int, user_service: UserService = Depends(get_user_service),
) -> UserModel:
    user: Optional[dict] = user_service.get_user_detail(item_id=user_id)
    if not user:
        # Если пользователь не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="user not found")
    return UserModel(**user)


@router.patch(
    path="/me",
    response_model=UserModel,
    summary="Обновить данные определенного пользователя",
    tags=["users"],
)
def user_update(
    user: UserPatch, user_service: UserService = Depends(get_user_service),
) -> UserModel:
    user_check: Optional[dict] = user_service.check_user_name(username=user.username)
    if user_check and user_check != user.id:
        # Если пользователь с таким именем существует, отдаём 406 статус
        raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE, detail="username exists")
    user: dict = user_service.update_user_detail(user=user)
    return UserModel(**user)

