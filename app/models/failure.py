from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base


class Failure(Base):
    __tablename__ = "failures"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    gear_type = Column(String, index=True)
    failure_on = Column(DateTime, index=True)
    repaired_on = Column(DateTime)
    duration = Column(Float)
    category = Column(String)
    cause = Column(String)
    department = Column(String)
    lightning_index = Column(Float, default=0.0)
