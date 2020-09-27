from aiogram import Router, types

router = Router()


@router.message(commands=["start", "help"])
async def start(message: types.Message):
    await message.answer(
        "👋 *Hi there!* I can offer advanced protection for you Telegram chat. Add me in a chat or check out my source code: https://github.com/crinny/gatee"
    )
