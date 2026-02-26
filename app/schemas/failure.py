from datetime import datetime

from pydantic import BaseModel


class FailureOut(BaseModel):
    id: int
    location: str
    gear_type: str
    failure_on: datetime
    repaired_on: datetime | None
    duration: float | None
    category: str | None
    cause: str | None
    department: str | None
    lightning_index: float | None

    class Config:
        from_attributes = True
