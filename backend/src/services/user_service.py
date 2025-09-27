from typing import Dict, List
from uuid import UUID
from backend.src.models.user import User, UserCreate

class UserService:
    def __init__(self):
        self.users: Dict[UUID, User] = {}

    def create_user(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def get_user_by_id(self, user_id: UUID) -> User | None:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        for user in self.users.values():
            if user.email == email:
                return user
        return None
