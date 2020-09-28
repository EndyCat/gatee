from aiogram import Router, types

from ..database.models import Chat, ChatSettings
from ..filters import bot_is_group_admin, new_chat_members
from ..punishment_determiner import determine_punishment
from ..punishment_executor import PunishmentExecutor
from ..utils.telegram import is_group_admin

router = Router()


@router.message(new_chat_members)
async def new_chat_members_(message: types.Message):
    chat = await Chat.get_chat(message.chat.id)
    settings: ChatSettings = chat.settings

    if (
        chat is None
        or not await bot_is_group_admin(message)
        or is_group_admin(message.chat.id, message.from_user.id)
    ):
        return

    new_chat_members_filtered = filter(lambda m: not m.is_bot, message.new_chat_members)

    for user in new_chat_members_filtered:
        punishment = await determine_punishment(user, settings)
        if punishment is None:
            continue

        executor = PunishmentExecutor(
            message.chat, user, db_chat=chat, punishment=punishment
        )
        await executor.execute()
