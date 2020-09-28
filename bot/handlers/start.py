from aiogram import Router, types
from aiogram.api.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..utils.telegram import get_me

router = Router()


@router.message(commands=["start", "help"])
async def start(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        return

    me = await get_me()
    add_to_chat = InlineKeyboardButton(
        text="Add to chat", url=f"https://t.me/{me.username}?startgroup=start"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[add_to_chat]])

    await message.answer(
        "👋 *Hi there!* I can offer advanced protection for you Telegram chat. Add me to a chat or check out my source code: https://github.com/crinny/gatee",
        reply_markup=keyboard,
    )
