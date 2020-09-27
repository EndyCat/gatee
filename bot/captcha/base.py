import asyncio
from abc import ABC, abstractmethod

from aiogram.api.methods import DeleteMessage, KickChatMember
from aiogram.api.types import Chat, Message, User

from ..database.models import CaptchaChallenge


class BaseCaptchaSender(ABC):
    def __init__(self, chat: Chat, user: User):
        self.chat = chat
        self.user = user

    @abstractmethod
    async def send(self, challenge: CaptchaChallenge) -> Message:
        raise NotImplementedError


async def start_captcha_challenge_timer(
    challenge: CaptchaChallenge, time: float
) -> None:
    await asyncio.sleep(time)

    if await CaptchaChallenge.find_one({"uuid": challenge.uuid}):
        await KickChatMember(chat_id=challenge.chat_id, user_id=challenge.user_id)
        await DeleteMessage(chat_id=challenge.chat_id, message_id=challenge.message_id)
        await challenge.delete()
