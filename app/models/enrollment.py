from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class Enrollment(Base):
    __tablename__ = "Enrollments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("Students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("Courses.id"), nullable=False)
