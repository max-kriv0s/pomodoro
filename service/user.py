from dataclasses import dataclass
from random import choice
import string

from repository.user import UserRepository
from schema.user import UserLoginSchema


@dataclass
class UserService:
    user_repository: UserRepository
    
    def create_user(self, username: str, password: str) -> UserLoginSchema:
        access_token = self._generate_access_token()
        user = self.user_repository.create_user(username=username, password=password, access_token=access_token)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)
    
    def _generate_access_token(self) -> str:
        return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(10)) 