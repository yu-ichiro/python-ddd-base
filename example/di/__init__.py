from typing import Type, TypeVar, Union

from inject import Binder

from example.domain.user.IUserRepo import IUserRepo
from example.infrastructures.mock import MockUserRepo
from example.infrastructures.sqlite import SqliteUserRepo

T = TypeVar('T')


def check_and_bind(binder: Binder, cls: Type[T], ins: Union[Type[T], T]):
    exp = None
    try:
        is_sub = issubclass(ins, cls)
    except TypeError as e:
        is_sub = False
        exp = e
    try:
        is_ins = isinstance(ins, cls)
    except TypeError as e:
        is_ins = False
        exp = e
    if is_ins or is_sub:
        binder.bind(cls, ins)
    else:
        raise exp or TypeError(f"{ins} is neither subclass or instance of {cls}")


def mock_config(binder: Binder):
    check_and_bind(binder, IUserRepo, MockUserRepo())


def sqlite_config(binder: Binder):
    check_and_bind(binder, IUserRepo, SqliteUserRepo())


def sqlite_file_config(binder: Binder):
    check_and_bind(binder, IUserRepo, SqliteUserRepo("sqlite:///example/di/sample.db3"))
