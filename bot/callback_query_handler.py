from abc import ABC, abstractmethod
from typing import List

from aiogram.api.types import CallbackQuery
from aiogram.dispatcher.handler import CallbackQueryHandler
from pydantic.error_wrappers import ValidationError

from .database.models import Chat, ChatSettings


class AdvancedCallbackQueryHandler(CallbackQueryHandler, ABC):
    chat: Chat
    settings: ChatSettings
    query_raw: str
    query = None

    query_model = None

    @abstractmethod
    async def post_handle(self):
        raise NotImplementedError

    async def handle(self):
        self.chat = await Chat.get_chat(self.event.message.chat.id)
        if self.chat is None:
            return

        self.chat = self.chat
        self.settings = self.chat.settings

        self.query_raw = self.event.data
        query = self.query_raw.split("_")
        if len(query) <= 1 and self.query_model is not None:
            return

        if self.query_model is not None:
            self.query = list_to_model(query, self.query_model)

        await self.post_handle()


def list_to_model(data: List[str], model):
    if len(model.__fields__) != len(data):
        raise ValueError(f"Excepted {len(model.__fields__)} values, got {len(data)}")

    values = dict(zip(model.__fields__, data))
    return model(**values)


def matches_model(model):
    def check(query: CallbackQuery) -> bool:
        try:
            list_to_model(query.data.split("_"), model)
            return True
        except (ValueError, ValidationError):
            return False

    return check
