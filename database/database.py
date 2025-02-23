from typing import Optional
from sqlalchemy.orm import DeclarativeBase,declared_attr


class Base(DeclarativeBase):
    id: any
    __name__: str
    
    __allow_unmapper__ = True
    
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

