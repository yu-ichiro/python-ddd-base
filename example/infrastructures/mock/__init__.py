from typing import Optional, List

from example.domain.user import User, UserID, Name, Kana, BulkRequest
from example.domain.user.IUserRepo import IUserRepo


class MockUserRepo(IUserRepo):
    def __init__(self):
        self._counter = 0
        user_id = UserID(value='dummy')
        self._data = {
            user_id.value: User(
                id=UserID(value='dummy'),
                name=Name(
                    last='スミス',
                    first='祐一郎',
                    last_kana=Kana('スミス'),
                    first_kana=Kana('ユウイチロウ')
                )
            )
        }

    def get_user(self, user_id: UserID) -> Optional[User]:
        return self._data.get(user_id.value) or None

    def list_users(self, request: BulkRequest = BulkRequest(limit=50, offset=0)) -> List[User]:
        return list(self._data.values())[request.offset:request.offset+request.limit]

    def save_user(self, user: User) -> bool:
        self._data[user.id.value] = user
        return True

    def create_user(self, name: Name) -> User:
        new_user_id = UserID(value=str(self._counter))
        if new_user_id.value in self._data:
            raise RuntimeError('id collision')
        new_user = User(id=new_user_id, name=name)
        self._data[new_user_id.value] = new_user
        self._counter += 1
        return new_user

    def exist_user(self, user_id: UserID) -> bool:
        return user_id.value in self._data

