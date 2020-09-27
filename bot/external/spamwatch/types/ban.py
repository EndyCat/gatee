from datetime import datetime

from pydantic import BaseModel


class Ban(BaseModel):
    id: int
    reason: str
    date: datetime
    admin: int
