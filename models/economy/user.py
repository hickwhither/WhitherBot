from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList, MutableDict, MutableSet
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import *

UserBase = declarative_base()

class UserModel(UserBase):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    credit:Mapped[int] = mapped_column(BigInteger, default=0)

    zoo:Mapped[dict] = mapped_column(MutableDict.as_mutable(PickleType), default={})
    # animal: {'asd': {'id': 'asd', 'name': str, 'level': int, 'amount': 0, weapon:'wp_id'}}
    team:Mapped[list] = mapped_column(MutableList.as_mutable(PickleType), default=[])
    # ['id', 'id']
    
    inventory:Mapped[list] = mapped_column(MutableList.as_mutable(PickleType), default=[])
    # item: {'type': 'Weapon', 'id': '71UWALS'}
