from typing import Annotated
from fastapi import APIRouter, Depends

from app.dependency import get_user_service
from app.schema import UserCreateSchema, UserLoginSchema
from app.service import UserService


router = APIRouter(prefix="/user", tags=["user"])


@router.post("")
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserLoginSchema:
    return await user_service.create_user(
        username=body.username, password=body.password
    )
