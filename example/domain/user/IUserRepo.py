from abc import ABC, abstractmethod
from typing import Optional, List

from example.domain.user import User, UserID, BulkRequest


class IUserRepo(ABC):
    @abstractmethod
    def get_user(self, user_id: UserID) -> Optional[User]:
        ...

    @abstractmethod
    def list_users(self, request: BulkRequest = BulkRequest(limit=50, offset=0)) -> List[User]:
        ...

    @abstractmethod
    def save_user(self, user: User) -> bool:
        ...

    @abstractmethod
    def exist_user(self, user_id: UserID) -> bool:
        ...
