from sqlalchemy import Column, Integer, String
from .base import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    nom = Column(String, nullable=False)
    password = Column(String, nullable=False)
