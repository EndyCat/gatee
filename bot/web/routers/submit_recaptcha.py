import os

from aiogram import Bot
from aiogram.api.types import ChatPermissions
from fastapi import APIRouter, HTTPException, Request

from ...database.models import CaptchaChallenge
from ...external import ReCaptcha
from ..models import RecaptchaResultModel

router = APIRouter()


@router.post("/submit")
async def submit(recaptcha_response: RecaptchaResultModel, request: Request):
    challenge = await CaptchaChallenge.get_challenge(recaptcha_response.uuid)
    bot: Bot = request.app.state.bot

    if not challenge:
        raise HTTPException(
            404, f"Challenge with UUID {recaptcha_response.uuid} doesn't exist"
        )

    async with ReCaptcha(os.getenv("RECAPTCHA_SECRET")) as recaptcha:
        verification = await recaptcha.verify(recaptcha_response.g_recaptcha_response)

        if verification.challenge_ts:
            await bot.restrict_chat_member(
                challenge.chat_id,
                challenge.user_id,
                ChatPermissions(can_send_messages=True),
            )
            await challenge.delete()
            await bot.delete_message(challenge.chat_id, challenge.message_id)

        return {"success": verification.challenge_ts is not None}
