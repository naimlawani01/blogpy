from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, TEXT
from .base import Base

class Article(Base):
    __tablename__="article"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(TEXT, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    img = Column(String, nullable=True)
    create_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')