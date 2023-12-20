from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UUID, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Admin(Base):
    __tablename__ = "admin"

    id = Column(UUID, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    last_login = Column(Date, nullable=True)
    is_super_user = Column(Boolean, default=False, nullable=True)

class User(Base):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True, index=True)
    nama = Column(String)
    telp = Column(String)