from uuid import uuid4

from pydantic import BaseModel, BaseConfig


class Base(BaseModel):
    class Config(BaseConfig):
        orm_mode = True


class EntityBase(Base):
    ...


class ValueBase(Base):
    ...


class IDBase(ValueBase):
    value: str

    @classmethod
    def generate(cls):
        return cls(value=str(uuid4()))
