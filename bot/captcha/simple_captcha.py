import random

from aiogram.api.methods import SendMessage
from aiogram.api.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..utils.telegram import mention
from . import BaseCaptchaSender


class SimpleCaptchaSender(BaseCaptchaSender):
    async def send(self, challenge):
        return await SendMessage(
            chat_id=self.chat.id,
            text=f"🤖 {mention(self.user)}, please confirm you are *not a robot*!",
            parse_mode="Markdown",
            reply_markup=self._make_keyboard(challenge),
        )

    @staticmethod
    def _make_keyboard(challenge):
        buttons = [
            [
                InlineKeyboardButton(
                    text="I am a robot",
                    callback_data=f"captcha_simple_{challenge.uuid}_robot",
                ),
                InlineKeyboardButton(
                    text="I am a human",
                    callback_data=f"captcha_simple_{challenge.uuid}_human",
                ),
            ],
        ]
        random.shuffle(buttons)

        return InlineKeyboardMarkup(inline_keyboard=buttons)
