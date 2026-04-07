from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Course(Base):
    __tablename__ = "Courses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    credits = Column(Integer, nullable=False)
    instructor_id = Column(Integer, ForeignKey("Instructors.id"), nullable=False)
    students = relationship(
        "Student", secondary="Enrollments", back_populates="courses"
    )
    instructor = relationship("Instructor", back_populates="courses")
