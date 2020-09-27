from aiogram import Router
from aiogram.api.methods import DeleteMessage, KickChatMember, RestrictChatMember
from aiogram.api.types import ChatPermissions
from pydantic import BaseModel
from typing_extensions import Literal

from ..callback_query_handler import AdvancedCallbackQueryHandler, matches_model
from ..database.models import CaptchaChallenge
from ..enums import Captchas

router = Router()


class CaptchaAnswerQueryData(BaseModel):
    type: Literal["captcha"]
    captcha_type: str
    uuid: str
    answer: str


@router.callback_query(matches_model(CaptchaAnswerQueryData))
class CaptchaAnswerHandler(AdvancedCallbackQueryHandler):
    query_model = CaptchaAnswerQueryData

    async def post_handle(self):
        query = self.query

        captcha_types = {"emoji": Captchas.EMOJI, "simple": Captchas.SIMPLE}
        captcha_type = captcha_types[query.captcha_type]

        challenge = await CaptchaChallenge.get_challenge(query.uuid)
        if not self.query_matches_challenge(challenge):
            return

        is_answer_correct = (
            query.answer == challenge.correct_emoji_answer
            if captcha_type == Captchas.EMOJI
            else query.answer == "human"
        )

        if is_answer_correct:
            await RestrictChatMember(
                chat_id=challenge.chat_id,
                user_id=challenge.user_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                ),
            )
        else:
            await KickChatMember(chat_id=challenge.chat_id, user_id=challenge.user_id)

        await DeleteMessage(chat_id=challenge.chat_id, message_id=challenge.message_id)
        await challenge.delete()

    def query_matches_challenge(self, challenge: CaptchaChallenge) -> bool:
        return (
            challenge is not None
            and challenge.user_id == self.event.from_user.id
            and challenge.chat_id == self.event.message.chat.id
        )
