import re
from typing import Optional

from pydantic import Field

from example.domain import EntityBase, ValueBase, IDBase


class Kana(str):
    pattern: re.Pattern = re.compile(r'^[ヴァー−・ア-ン]+$')

    def is_kana(self):
        return self.pattern.match(self) is not None


class Name(ValueBase):
    first: str
    last: str
    first_kana: Kana
    last_kana: Kana

    other: Optional[str] = None
    other_kana: Optional[Kana] = None

    def __init__(
            self,
            first: str,
            last: str,
            first_kana: Kana,
            last_kana: Kana,
            other: Optional[str] = None,
            other_kana: Optional[Kana] = None
    ):
        super().__init__(
            first=first,
            last=last,
            first_kana=first_kana,
            last_kana=last_kana,
            other=other,
            other_kana=other_kana
        )
        if not first or not last:
            raise ValueError('Firstname and lastname are both required')
        if not first_kana or not last_kana:
            raise ValueError('firstname_kana and lastname_kana are both required')
        if not first_kana.is_kana() or not last_kana.is_kana() or (other_kana and not other_kana.is_kana()):
            raise ValueError('*_kana must be Katakana')


class BulkRequest(ValueBase):
    limit: int = Field(50, description="Number of results to limit to", example=50, ge=0)
    offset: int = Field(0, description="Number of results to skip", example=0, ge=0)


class UserID(IDBase):
    ...


class User(EntityBase):
    id: UserID
    name: Name

    @classmethod
    def create(cls, name: Name):
        return cls(id=UserID.generate(), name=name)
