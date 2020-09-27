from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.api.types import CallbackQuery, Message

from ..utils.telegram import is_group_admin


class GroupAdminMiddleware(BaseMiddleware[Union[Message, CallbackQuery]]):
    async def __call__(
        self,
        handler: Callable[
            [Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]
        ],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        chat_id = event.chat.id if isinstance(event, Message) else event.message.chat.id
        if await is_group_admin(chat_id, event.from_user.id):
            return await handler(event, data)

        await event.answer("You need to be an administrator to do that!")
