from typing import Optional, List, Type, cast
from uuid import uuid4

from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from example.domain.user import User, UserID, Name, Kana, BulkRequest
from example.domain.user.IUserRepo import IUserRepo


ORMBase = declarative_base()


class UserORM(ORMBase):
    __tablename__ = 'users'

    id = Column(String(64), primary_key=True)
    first_name = Column(Text)
    first_kana = Column(Text)
    last_name = Column(Text)
    last_kana = Column(Text)
    other_name = Column(Text)
    other_kana = Column(Text)

    def to_eo(self):
        return User(
            id=UserID(value=self.id),
            name=Name(
                first=self.first_name,
                last=self.last_name,
                first_kana=Kana(self.first_kana),
                last_kana=Kana(self.last_kana),
                other=self.other_name,
                other_kana=Kana(self.other_name)
            )
        )

    def set_user_data(self, name: Optional[Name] = None):
        if name:
            self.first_name = name.first
            self.first_kana = name.first_kana
            self.last_name = name.last
            self.last_kana = name.last_kana
            self.other_name = name.other
            self.other_kana = name.other_kana


class SqliteUserRepo(IUserRepo):
    engine: Engine
    session_cls: Type[Session]

    def __init__(self, url: str = 'sqlite://'):
        self.engine = create_engine(url)
        ORMBase.metadata.create_all(self.engine)
        self.session_cls = cast('Type[Session]', scoped_session(sessionmaker(bind=self.engine)))

    def get_user(self, user_id: UserID) -> Optional[User]:
        session = self.session_cls()
        user: UserORM = session.query(UserORM).filter(UserORM.id == user_id.value).first()
        return user.to_eo() or None

    def list_users(self, request: BulkRequest = BulkRequest(limit=50, offset=0)) -> List[User]:
        session = self.session_cls()
        return [
            user.to_eo()
            for user in session.query(UserORM).limit(request.limit).offset(request.offset)
        ]

    def save_user(self, user: User) -> bool:
        session = self.session_cls()
        user_orm: UserORM = session.query(UserORM).filter(UserORM.id == user.id.value).first()
        if not user_orm:
            return False
        user_orm.set_user_data(name=user.name)
        session.add(user_orm)
        session.commit()
        return True

    def create_user(self, name: Name) -> User:
        session = self.session_cls()
        user_orm = UserORM()
        user_orm.id = str(uuid4())
        user_orm.set_user_data(name=name)
        session.add(user_orm)
        session.commit()
        session.refresh(user_orm)
        return user_orm.to_eo()

    def exist_user(self, user_id: UserID) -> bool:
        return bool(self.get_user(user_id))

