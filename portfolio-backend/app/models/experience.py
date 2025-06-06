import enum
from sqlalchemy import Column, Integer, String, Date, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ExperienceType(str, enum.Enum):
    work = "work"
    internship = "internship"


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    type = Column(Enum(ExperienceType), nullable=False)  # only work/internship

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False)

    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="experiences")
