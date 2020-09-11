from typing import Optional, List

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from example.domain.user import Name, Kana, BulkRequest, User, UserID
from example.usecase import ValueTransferObjectBase, UserUseCase

user_router = APIRouter()


class NameVTO(ValueTransferObjectBase):
    first: str = Field(..., example="太郎")
    last: str = Field(..., example="田中")
    first_kana: str = Field(..., regex=Kana.pattern.pattern, example="タロウ")
    last_kana: str = Field(..., regex=Kana.pattern.pattern, example="タナカ")

    other: Optional[str] = Field(None, example="ジョン")
    other_kana: Optional[str] = Field(None, example="ジョン")

    @classmethod
    def from_vo(cls, name: Name):
        return cls(
            first=name.first,
            last=name.last,
            first_kana=str(name.first_kana),
            last_kana=str(name.last_kana),
            other=name.other,
            other_kana=name.other_kana and str(name.other_kana),
        )

    def to_vo(self):
        return Name(
            first=self.first,
            last=self.last,
            first_kana=Kana(self.first_kana),
            last_kana=Kana(self.last_kana),
            other=self.other,
            other_kana=self.other_kana and Kana(self.other_kana),
        )


class UserVTO(ValueTransferObjectBase):
    id: str = Field(..., example="0")
    name: NameVTO = Field(...)

    @classmethod
    def from_eo(cls, user: User):
        return cls(id=user.id.value, name=NameVTO.from_vo(user.name))

    def to_eo(self):
        return User(id=UserID(value=self.id), name=self.name.to_vo())


class UserListResult(BaseModel):
    users: List[UserVTO]


@user_router.get('/users', response_model=UserListResult)
async def list_users(limit: int = Query(50, ge=0), offset: int = Query(0, ge=0)) -> UserListResult:
    use_case = UserUseCase()

    result = use_case.list_users(BulkRequest(limit=limit, offset=offset))
    return UserListResult(users=[UserVTO.from_eo(user) for user in result.users])


class UserCreateRequest(BaseModel):
    name: NameVTO


class UserCreateResult(BaseModel):
    id: str
    name: NameVTO


@user_router.post('/user', response_model=UserCreateResult)
async def create_user(request: UserCreateRequest) -> UserCreateResult:
    use_case = UserUseCase()

    result = use_case.create_user(request.name.to_vo())
    return UserCreateResult(id=result.id, name=NameVTO.from_vo(result.name))


class ChangeNameRequest(BaseModel):
    id: str = Field(..., example="0")
    name: NameVTO = Field(..., example=NameVTO(first="太郎", last="田中", first_kana="タロウ", last_kana="タナカ"))


class ChangeNameResult(BaseModel):
    id: str = Field(..., example="0")
    old_name: NameVTO = Field(...)
    new_name: NameVTO = Field(..., example=NameVTO(first="太郎", last="田中", first_kana="タロウ", last_kana="タナカ"))


@user_router.put('/user/change_name', response_model=ChangeNameResult)
async def change_name(request: ChangeNameRequest) -> ChangeNameResult:
    use_case = UserUseCase()

    result = use_case.change_name(UserID(value=request.id), request.name.to_vo())
    return ChangeNameResult(
        id=request.id,
        old_name=NameVTO.from_vo(result.old_name),
        new_name=NameVTO.from_vo(result.new_name)
    )
