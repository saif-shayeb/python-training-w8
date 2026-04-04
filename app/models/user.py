from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100),nullable=False)
    password = Column(String(500),nullable=False)
    role = Column(String(100),nullable=False)
    email = Column(String(100),nullable=False)
    student = relationship('Student', back_populates='user', uselist=False)
