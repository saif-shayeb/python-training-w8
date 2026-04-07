from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Student(Base):
    __tablename__ = "Students"
    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("Users.id"), unique=True, nullable=False)
    user = relationship("User", back_populates="student")

    name = Column(String(100), nullable=False)
    gpa = Column(Float, nullable=False)

    courses = relationship("Course", secondary="Enrollments", back_populates="students")
