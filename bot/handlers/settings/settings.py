from typing import Optional

from aiogram import Router, types
from aiogram.api.methods import EditMessageText
from aiogram.api.types import InlineKeyboardButton

from ...database.models import Chat, ChatSettings
from ...middlewares import GroupAdminMiddleware
from ...utils.keyboard import make_violation_selection_keyboard

router = Router()
router.message.middleware(GroupAdminMiddleware())


@router.message(commands=["settings"])
async def settings_menu(message: types.Message):
    main_menu_keyboard = await make_settings_menu_keyboard(message.chat.id)
    if main_menu_keyboard is None:
        return

    await message.answer(
        "🛠 Here are the settings for this chat", reply_markup=main_menu_keyboard
    )


@router.callback_query(lambda q: q.data.endswith("main"))
async def settings_menu_callback(query: types.CallbackQuery):
    query_message = query.message

    main_menu_keyboard = await make_settings_menu_keyboard(query_message.chat.id)
    if main_menu_keyboard is None:
        return

    await EditMessageText(
        text="🛠 Here are the settings for this chat",
        chat_id=query_message.chat.id,
        message_id=query_message.message_id,
        parse_mode="",
        reply_markup=main_menu_keyboard,
    )


async def make_settings_menu_keyboard(
    chat_id: int,
) -> Optional[types.InlineKeyboardMarkup]:
    chat = await Chat.get_chat(chat_id)

    if chat is None:
        return

    settings: ChatSettings = chat.settings
    punishments = settings.sort_punishments_by_weight(
        ignore_none_punishments=False, sort_by_length=True
    )

    keyboard = make_violation_selection_keyboard(punishments)
    keyboard.inline_keyboard[-1].append(
        InlineKeyboardButton(
            text="📅 Creation date settings", callback_data="CreationDateSettings"
        )
    )

    return keyboard
