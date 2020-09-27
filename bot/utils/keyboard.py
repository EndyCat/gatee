from typing import List

from aiogram.api.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..enums import Punishment
from ..utils.display import (
    punishments_main_menu_display_name,
    punishments_selection_menu_display_name,
    violations_display_name,
)
from ..utils.misc import chunks, dict_chunks


def make_violation_selection_keyboard(
    punishments: List[Punishment],
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{violations_display_name[punishment.name]} - {punishments_main_menu_display_name[punishment.type]}",
                callback_data=punishment.name,
            )
            for punishment in chunk
        ]
        for chunk in chunks(punishments, 2)
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


def make_punishment_selection_keyboard(violation_type: str) -> InlineKeyboardMarkup:
    menu = {**punishments_selection_menu_display_name, "🔙 Go back": "main"}

    buttons = [
        [
            InlineKeyboardButton(text=k, callback_data=f"{violation_type}_{v}")
            for k, v in chunk.items()
        ]
        for chunk in dict_chunks(menu, 2)
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


def make_mute_time_selection_keyboard(violation_type: str) -> InlineKeyboardMarkup:
    time = {
        "5 minutes": 5,
        "10 minutes": 10,
        "30 minutes": 30,
        "1 hour": 60,
        "2 hours": 120,
    }

    buttons = [
        [
            InlineKeyboardButton(
                text=text, callback_data=f"{violation_type}_mute_{minutes}",
            )
            for text, minutes in chunk.items()
        ]
        for chunk in dict_chunks(time, 3)
    ]

    buttons[-1].append(
        InlineKeyboardButton(text="🔙 Go back", callback_data=violation_type)
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


def make_creation_date_selection_keyboard() -> InlineKeyboardMarkup:
    months = {"1 month": 1, "2 months": 2, "3 months": 3, "6 months": 6}

    buttons = [
        [
            InlineKeyboardButton(text=text, callback_data=f"creationdate_{month}",)
            for text, month in chunk.items()
        ]
        for chunk in dict_chunks(months, 2)
    ]

    buttons[-1].append(InlineKeyboardButton(text="🔙 Go back", callback_data="main"))
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


def make_captcha_type_selection_keyboard(violation_type: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Simple", callback_data=f"{violation_type}_captcha_simple"
            ),
            InlineKeyboardButton(
                text="Emoji", callback_data=f"{violation_type}_captcha_emoji"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ReCaptcha", callback_data=f"{violation_type}_captcha_recaptcha"
            ),
            InlineKeyboardButton(text="🔙 Go back", callback_data=violation_type),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard
