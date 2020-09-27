from typing import Optional

from aiogram.api.types import Message

from ..utils.telegram import get_me


async def added_to_group(message: Message) -> Optional[bool]:
    if message.new_chat_members is not None:
        me = await get_me()

        for member in message.new_chat_members:
            if member.id == me.id:
                return True

        return False


async def new_chat_members(message: Message) -> bool:
    return await added_to_group(message) is False
