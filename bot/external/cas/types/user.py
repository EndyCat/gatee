from datetime import datetime
from typing import List

from pydantic import BaseModel


class User(BaseModel):
    offenses: int
    messages: List[str]
    time_added: datetime
