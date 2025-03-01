from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from client import GoogleClient, YandexClient
from exception import (
    TokenExpiredException,
    TokenNotCorrectException,
    UserNotCorrectPasswordException,
    UserNotFoundException,
)
from models import UserProfile
from repository import UserRepository
from schema import UserLoginSchema

from schema import UserCreateSchema
from settings import Settings
from utils import verify_password


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    def google_auth(self, code: str):
        user_data = self.google_client.get_user_info(code=code)

        if user := self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name,
        )
        created_user = self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def yandex_auth(self, code: str):
        user_data = self.yandex_client.get_user_info(code=code)
        if user := self.user_repository.get_user_by_email(
            email=user_data.default_email
        ):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            yandex_access_token=user_data.access_token,
            email=user_data.default_email,
            name=user_data.name,
        )
        created_user = self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user=user, password=password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if not verify_password(password=password, hashed_pass=user.password):
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: str) -> str:
        expires_date_unix = (
            datetime.now(timezone.utc)
            + timedelta(days=self.settings.ACCESS_TOKEN_LIFETIME)
        ).timestamp()
        encode = {"user_id": user_id, "exp": expires_date_unix}
        token = jwt.encode(
            encode, self.settings.JWT_SECRET_KEY, algorithm=self.settings.JWT_ALGORITHM
        )
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                access_token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ALGORITHM],
            )
        except JWTError as e:
            print(e.args)
            raise TokenNotCorrectException

        if payload["exp"] < datetime.now(timezone.utc).timestamp():
            raise TokenExpiredException

        return payload["user_id"]
