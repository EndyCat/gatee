from typing import Union

from aiocache import cached
from aiogram import Bot, Dispatcher
from aiogram.api.methods import GetChatMember
from aiogram.api.types import User


@cached()
async def get_me() -> User:
    return await Bot.get_current().get_me()


@cached(ttl=30)
async def is_group_admin(chat_id: Union[int, str], user_id: int) -> bool:
    chat_member = await GetChatMember(chat_id=chat_id, user_id=user_id)

    return chat_member.status in ["creator", "administrator"]


def mention(user: User) -> str:
    if user.username:
        return f"@{user.username}"

    full_name = user.first_name
    if user.last_name:
        full_name += f" {user.last_name}"

    return f"[{full_name}](tg://user?id={user.id})"


def include_routers(dp: Dispatcher):
    dp.include_router("bot.handlers.start:router")
    dp.include_router("bot.handlers.new_chat_members:router")
    dp.include_router("bot.handlers.added_to_group:router")
    dp.include_router("bot.handlers.settings.settings:router")
    dp.include_router("bot.handlers.settings.callbacks:router")
    dp.include_router("bot.handlers.captcha:router")
