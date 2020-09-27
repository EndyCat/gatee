from pydantic import BaseModel, Field


class RecaptchaResultModel(BaseModel):
    uuid: str
    g_recaptcha_response: str = Field(..., alias="g-recaptcha-response")
