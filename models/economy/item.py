from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList, MutableDict, MutableSet
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import *

ItemBase = declarative_base()


class Weapon(ItemBase):
    __tablename__ = "weapons"
    id = mapped_column(String, primary_key=True)
    
    weapon_id = mapped_column(String, nullable=False)
    quality = mapped_column(Float, nullable=False)