from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(500), nullable=False)
    role = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    profile_pic_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    student = relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    instructor = relationship(
        "Instructor",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
