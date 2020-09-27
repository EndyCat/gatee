from aiogram.api.types import Message

from ..utils.telegram import get_me, is_group_admin


async def bot_is_group_admin(message: Message) -> bool:
    me = await get_me()
    return await is_group_admin(message.chat.id, me.id)
