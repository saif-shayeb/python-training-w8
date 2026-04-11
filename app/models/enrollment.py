from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from database import Base


class Enrollment(Base):
    __tablename__ = "Enrollments"
    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_enrollment_student_course"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(
        Integer, ForeignKey("Students.id", ondelete="CASCADE"), nullable=False
    )
    course_id = Column(
        Integer, ForeignKey("Courses.id", ondelete="CASCADE"), nullable=False
    )
