from typing import List
from uuid import uuid4

import inject

from example.domain.user import Name, UserID, BulkRequest, User
from example.domain import Base
from example.domain.user.IUserRepo import IUserRepo


class ValueTransferObjectBase(Base):
    ...


class UserCreatedResult(ValueTransferObjectBase):
    id: str
    name: Name


class UserListResult(ValueTransferObjectBase):
    users: List[User]


class ChangeNameResult(ValueTransferObjectBase):
    old_name: Name
    new_name: Name


class UserUseCase:
    repo: IUserRepo = inject.attr(IUserRepo)

    def create_user(self, name: Name) -> UserCreatedResult:
        user = User.create(name)
        self.repo.save_user(user)
        return UserCreatedResult(
            id=user.id.value,
            name=user.name
        )

    def list_users(self, request: BulkRequest) -> UserListResult:
        return UserListResult(users=self.repo.list_users(request))

    def change_name(self, user_id: UserID, new_name: Name) -> ChangeNameResult:
        user = self.repo.get_user(user_id)
        if not user:
            raise RuntimeError('User not found')
        old_name = user.name
        user.name = new_name
        if not self.repo.save_user(user):
            raise RuntimeError('Save user failed')
        return ChangeNameResult(
            new_name=new_name,
            old_name=old_name
        )
