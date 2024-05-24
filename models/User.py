from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Numeric
from .base import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    password = Column(String, nullable=False)
