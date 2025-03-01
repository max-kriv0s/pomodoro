from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from dependency import get_auth_service
from exception import UserNotCorrectPasswordException, UserNotFoundException
from schema import UserCreateSchema
from schema.user import UserLoginSchema
from service import UserService
from service.auth import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    dto: UserCreateSchema,
    auth_service: Annotated[UserService, Depends(get_auth_service)],
) -> UserLoginSchema:
    try:
        return auth_service.login(username=dto.username, password=dto.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)


@router.get("/login/google")
def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> RedirectResponse:
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get("/google")
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    return auth_service.google_auth(code=code)


@router.get("/login/yandex")
async def yandex_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> RedirectResponse:
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get("/yandex")
async def yandex_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    return auth_service.yandex_auth(code=code)
