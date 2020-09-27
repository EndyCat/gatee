from typing import NoReturn, Optional, Union

import umongo
from umongo import fields

from ..db import Instance
from . import ChatSettings

instance: umongo.Instance = Instance.get_current().instance


@instance.register
class Chat(umongo.Document):
    chat_id = fields.IntegerField(required=True, unique=True)
    settings = fields.EmbeddedField(ChatSettings)

    class Meta:
        collection_name = "chats"

    @staticmethod
    async def create_chat(
        chat_id: int, settings: ChatSettings
    ) -> Union["Chat", NoReturn]:
        chat = Chat(chat_id=chat_id, settings=settings)
        await chat.commit()
        return chat

    @staticmethod
    async def get_chat(chat_id: int) -> Optional["Chat"]:
        chat = await Chat.find_one({"chat_id": chat_id})
        return chat
