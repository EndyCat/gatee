from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ReCaptchaResponse(BaseModel):
    success: bool
    challenge_ts: Optional[datetime]
    hostname: Optional[str]
    error_codes: Optional[List[str]] = Field(alias="error-codes")
