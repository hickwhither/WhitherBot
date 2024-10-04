from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList, MutableDict, MutableSet
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import *

ItemBase = declarative_base()


class WeaponModel(ItemBase):
    __tablename__ = "weapons"
    id:Mapped[str] = mapped_column(String, primary_key=True)
    
    weapon_id:Mapped[str] = mapped_column(String, nullable=False)
    quality:Mapped[float] = mapped_column(Float, nullable=False)