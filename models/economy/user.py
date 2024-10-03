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

    pets = mapped_column(MutableDict.as_mutable(PickleType), default={})


"<:rokf:950607318922457128>"
"<:sus:952187167889817620>"
"<:aheg:945699029902319676>"
"<a:lick:945239728628834304>"
"<a:catshake:1291031455140679690>"
"<a:cvm:1291031442993709203>"
"<:uwu:949960339036987462>"
