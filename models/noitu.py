from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList, MutableDict, MutableSet
from sqlalchemy.orm import mapped_column, Mapped, relationship, sessionmaker
from sqlalchemy import *

Base = declarative_base()

class ChannelNoitu(Base):
    __tablename__ = "channelnoitu"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    words_used: Mapped[MutableList[str]] = mapped_column(MutableList.as_mutable(JSON), default=list)
    

DATABASE_URL = 'sqlite:///db/economy.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
