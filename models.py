from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.oop import calculate_level
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList, MutableDict, MutableSet
from sqlalchemy.orm import mapped_column, Mapped, relationship, sessionmaker
from sqlalchemy import *

Base = declarative_base()

class WeaponModel(Base):
    __tablename__ = "weapon"
    id:Mapped[str] = mapped_column(String, primary_key=True)

    weapon_id:Mapped[str] = mapped_column(String, nullable=False)
    quality:Mapped[float] = mapped_column(Float, nullable=False)
    
    lock:Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped['UserModel'] = relationship(back_populates="weapon")

    reroll_changes:Mapped[int] = mapped_column(Integer, default=0)
    reroll_attemps:Mapped[int] = mapped_column(Integer, default=0)

    def get_param(self):
        return {'id': self.weapon_id, 'quality': self.quality}

class UserModel(Base):
    __tablename__ = "user"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    credit:Mapped[int] = mapped_column(BigInteger, default=0)
    weapon_shards:Mapped[int] = mapped_column(BigInteger, default=0)

    zoo:Mapped[dict] = mapped_column(MutableDict.as_mutable(PickleType), default={})
    # animal: {'asd': {'id': 'asd', 'name': str, 'level': int, 'xp':int, 'amount': 0, weapon:'wp_id'}}
    team:Mapped[dict] = mapped_column(MutableDict.as_mutable(PickleType), default={'streak':0, 'max_streak':0})
    # {'name': str, 'pets': [{'pet': pet_id, 'weapon': weapon_id, 'xp': 0}]}
    weapon:Mapped[list['WeaponModel']] = relationship(back_populates="user")
    # item: [{'id': '71UWALS', 'weapon_id': ...}]
    gems:Mapped[dict] = mapped_column(MutableDict.as_mutable(PickleType), default={})
    # {'id': amount}

    hunt:Mapped[dict] = mapped_column(MutableDict.as_mutable(PickleType), default={'end': None})
    
    def full_update(self):
        self.zoo.update()
        self.team.update()
        self.gems.update()
        self.hunt.update()

            

DATABASE_URL = 'sqlite:///db/economy.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
