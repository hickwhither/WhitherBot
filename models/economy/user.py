from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList, MutableDict, MutableSet
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import *

UserBase = declarative_base()

class User(UserBase):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    credit = mapped_column(BigInteger, default=0)

    zoo = mapped_column(MutableDict.as_mutable(PickleType), default={})
    # animal: {'id': {'name': str, 'level': int, 'amount': 0, weapon:'wp_id'}}
    team = mapped_column(MutableList.as_mutable(PickleType), default=[])
    # ['id', 'id']
    
    inventory = mapped_column(MutableList.as_mutable(PickleType), default=[])
    # item: {'type': 'Weapon', 'id': '71UWALS'}
