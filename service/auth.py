from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from exception import (
    TokenExpiredException,
    TokenNotCorrectException,
    UserNotCorrectPasswordException,
    UserNotFoundException,
)
from models import UserProfile
from repository import UserRepository
from schema import UserLoginSchema

from settings import Settings
from utils import verify_password


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

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
