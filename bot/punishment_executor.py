import asyncio
from datetime import timedelta

from aiogram.api.methods import KickChatMember, RestrictChatMember, UnbanChatMember
from aiogram.api.types import Chat as TelegramChat
from aiogram.api.types import ChatPermissions, User

from .captcha import make_captcha_sender, start_captcha_challenge_timer
from .database.models import CaptchaChallenge, Chat
from .enums import Punishment, Punishments


class PunishmentExecutor:
    def __init__(
        self, chat: TelegramChat, user: User, db_chat: Chat, punishment: Punishment
    ):
        self.chat = chat
        self.db_chat = db_chat
        self.user = user

        self.punishment = punishment

    async def execute(self) -> None:
        mapping = {
            Punishments.BAN: self._ban,
            Punishments.KICK: self._kick,
            Punishments.MUTE: self._mute,
            Punishments.CAPTCHA: self._captcha,
        }
        try:
            await mapping[self.punishment.type]()  # noqa
        except KeyError:
            raise RuntimeError(
                f"No punishment executor found for punishment {self.punishment!r}."
            )

    async def _ban(self):
        await KickChatMember(chat_id=self.db_chat.chat_id, user_id=self.user.id)

    async def _kick(self):
        await KickChatMember(chat_id=self.db_chat.chat_id, user_id=self.user.id)
        await UnbanChatMember(chat_id=self.db_chat.chat_id, user_id=self.user.id)

    async def _mute(self):
        until_date = timedelta(
            seconds=self.db_chat.settings[self.punishment.db_name].mute_for
        )

        await RestrictChatMember(
            chat_id=self.db_chat.chat_id,
            user_id=self.user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date,
        )

    async def _captcha(self):
        await RestrictChatMember(
            chat_id=self.db_chat.chat_id,
            user_id=self.user.id,
            permissions=ChatPermissions(can_send_messages=False),
        )

        captcha_type = self.db_chat.settings[self.punishment.db_name].captcha_type
        captcha_sender = make_captcha_sender(captcha_type)(self.chat, self.user)

        challenge = await CaptchaChallenge.create_challenge(
            self.chat.id, self.user.id, message_id=None
        )
        sent_message = await captcha_sender.send(challenge)
        challenge.message_id = sent_message.message_id
        await challenge.commit()

        asyncio.create_task(
            start_captcha_challenge_timer(challenge, 120)
        )  # Ban the user if they fail to complete captcha after 2 minutes
