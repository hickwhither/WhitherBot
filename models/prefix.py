from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Prefix(Base):
    __tablename__ = 'prefixes'
    guild_id = Column(Integer, primary_key=True)
    prefix = Column(String)

DATABASE_URL = 'sqlite:///db/prefix.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)