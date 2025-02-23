from dataclasses import dataclass

from repository import UserRepository
from schema import UserLoginSchema
from service.auth import AuthService
from utils import get_hashed_password


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        hash_password = get_hashed_password(password)
        user = self.user_repository.create_user(
            username=username, password=hash_password
        )
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
