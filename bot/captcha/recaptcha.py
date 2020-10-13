import os

from aiogram.api.methods import SendMessage
from aiogram.api.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..utils.telegram import mention
from . import BaseCaptchaSender


class ReCaptchaSender(BaseCaptchaSender):
    async def send(self, challenge):
        scheme = os.getenv("WEB_SERVER_SCHEME")
        port = os.getenv("WEB_SERVER_PORT")
        alias = os.getenv("WEB_SERVER_ALIAS")

        host = f"{scheme}://{alias or os.getenv('WEB_SERVER_HOST')}"
        if port != 80 and not alias:
            host += f":{port}"

        buttons = [
            [
                InlineKeyboardButton(
                    text="Solve captcha",
                    url=f"{host}/recaptcha/{challenge.uuid}",
                ),
            ],
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        return await SendMessage(
            chat_id=self.chat.id,
            text=f"🤖 {mention(self.user)}, please confirm you are *not a robot*",
            reply_markup=keyboard,
            parse_mode="Markdown",
        )
