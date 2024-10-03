from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

from models.utils import merge_metadata

from user import UserBase

DATABASE_URL = 'sqlite:///db/economy.db'

def get_session():
    meta = merge_metadata(UserBase)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # session = SessionLocal()

    meta.create_all(bind=engine)
    return SessionLocal