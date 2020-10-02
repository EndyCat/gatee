from textwrap import dedent

from aiogram import Router, types

from ..database.models import Chat, ChatSettings, Punishment
from ..enums import Captchas, Punishments
from ..filters import added_to_group

router = Router()


@router.message(added_to_group)
async def added_to_group_(message: types.Message):
    text = dedent(
        """
        👋 *Hi there!* Thanks for adding me, I will help you fight spammers.
        In order for me to work, I need to be an admin with these permissions: *Delete messages, Ban users*.
        """
    )
    await message.answer(text)

    if await Chat.get_chat(message.chat.id):
        return

    settings = ChatSettings(
        cas_banned=Punishment(type=Punishments.BAN),
        spamwatch_banned=Punishment(type=Punishments.BAN),
        intellivoid_banned=Punishment(type=Punishments.BAN),
        account_creation_date_less_than_months=1,
        inappropriate_account_creation_date=Punishment(
            type=Punishments.CAPTCHA, captcha_type=Captchas.EMOJI
        ),
        rtl_characters_in_name=Punishment(type=None),
        url_in_name=Punishment(type=Punishments.CAPTCHA, captcha_type=Captchas.EMOJI),
    )
    await Chat.create_chat(message.chat.id, settings)
