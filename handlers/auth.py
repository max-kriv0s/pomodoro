from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from dependency import get_auth_service
from exception import UserNotCorrectPasswordException, UserNotFoundException
from schema import UserCreateSchema
from schema.user import UserLoginSchema
from service import UserService


router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/login')
def login(dto: UserCreateSchema, auth_service: Annotated[UserService, Depends(get_auth_service)]) -> UserLoginSchema:
    try:
        return auth_service.login(username=dto.username, password=dto.password)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )