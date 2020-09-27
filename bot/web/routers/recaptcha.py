import os

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

from ...database.models import CaptchaChallenge

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("bot", "web", "templates"))


@router.get("/{uuid}")
async def recaptcha(uuid: str, request: Request):
    if not await CaptchaChallenge.get_challenge(uuid):
        raise HTTPException(404, f"Challenge with UUID {uuid} doesn't exist")

    return templates.TemplateResponse(
        "recaptcha.html",
        {"request": request, "sitekey": os.getenv("RECAPTCHA_SITEKEY"), "uuid": uuid},
    )
