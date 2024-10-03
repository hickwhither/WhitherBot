from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList, MutableDict, MutableSet
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import *

ItemBase = declarative_base()

class Bag(ItemBase):
    __tablename__ = "bags"
    id = mapped_column(String, primary_key=True)
    parent_id = mapped_column(ForeignKey("users.id"))
    parent = relationship('User', back_populates="bag")

    alarm_level = mapped_column(Integer, default=0)
    alarm_durability = mapped_column(Float, default=1.0)
    protect_level = mapped_column(Integer, default=0)
    protect_durability = mapped_column(Float, default=1.0)

    items = mapped_column(MutableList.as_mutable(PickleType), default=[])
