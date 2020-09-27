from aiogram import Router
from aiogram.api.methods import EditMessageText
from pydantic import BaseModel, validator
from typing_extensions import Literal

from ...callback_query_handler import AdvancedCallbackQueryHandler, matches_model
from ...enums import Captchas, Punishments, ViolationType
from ...middlewares import GroupAdminMiddleware
from ...utils.display import (
    punishment_set_display_text,
    settings_changed_value_display_name,
    settings_description_display_name,
)
from ...utils.keyboard import (
    make_captcha_type_selection_keyboard,
    make_creation_date_selection_keyboard,
    make_mute_time_selection_keyboard,
    make_punishment_selection_keyboard,
)

router = Router()
router.callback_query.middleware(GroupAdminMiddleware())


class CaptchaTypeQueryData(BaseModel):
    violation_type: str
    punishment_type: Literal["captcha"]
    captcha_type: str


@router.callback_query(matches_model(CaptchaTypeQueryData))
class CaptchaTypeSelectionHandler(AdvancedCallbackQueryHandler):
    query_model = CaptchaTypeQueryData

    async def post_handle(self):
        mapping = {
            "simple": Captchas.SIMPLE,
            "emoji": Captchas.EMOJI,
            "recaptcha": Captchas.RECAPTCHA,
        }

        query = self.query

        self.settings[
            ViolationType[query.violation_type].value
        ].type = Punishments.CAPTCHA
        self.settings[ViolationType[query.violation_type].value].captcha_type = mapping[
            query.captcha_type
        ]
        await self.chat.commit()

        await self.event.answer(
            f"✅ OK, now I will show {query.captcha_type} captcha to the users {settings_changed_value_display_name[query.violation_type]}"
        )


class MuteTimeQueryData(BaseModel):
    violation_type: str
    punishment_type: Literal["mute"]
    time: int


@router.callback_query(matches_model(MuteTimeQueryData))
class MuteTimeSelectionHandler(AdvancedCallbackQueryHandler):
    query_model = MuteTimeQueryData

    async def post_handle(self):
        query = self.query

        self.settings[ViolationType[query.violation_type].value].type = Punishments.MUTE
        self.settings[ViolationType[query.violation_type].value].mute_for = (
            query.time * 60
        )
        await self.chat.commit()

        await self.event.answer(
            f"✅ OK, now I will mute the users {settings_changed_value_display_name[query.violation_type]} for {query.time} minutes"
        )


@router.callback_query(lambda q: q.data in ViolationType.__members__)
class ViolationSelectionHandler(AdvancedCallbackQueryHandler):
    async def post_handle(self):
        violation_type = self.event.data

        keyboard = make_punishment_selection_keyboard(violation_type)
        await EditMessageText(
            text=f"What should I do when *{settings_description_display_name[violation_type]}*?",
            chat_id=self.event.message.chat.id,
            message_id=self.event.message.message_id,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )


class PunishmentQueryData(BaseModel):
    violation_type: str
    action: str

    @validator("violation_type")
    def violation_type_exists(cls, violation_type: str):  # noqa
        if violation_type not in ViolationType.__members__:
            raise ValueError(f"Unknown violation type: {violation_type}")

        return violation_type

    @validator("action")
    def action_exists(cls, action: str):  # noqa
        if action not in [
            "ban",
            "kick",
            "mute",
            "captcha",
            "nothing",
        ]:
            raise ValueError(f"Unknown action: {action}")

        return action


@router.callback_query(matches_model(PunishmentQueryData))
class PunishmentSelectionHandler(AdvancedCallbackQueryHandler):
    query_model = PunishmentQueryData

    async def post_handle(self):
        action = self.query.action

        if action == "mute":
            return await self._handle_mute_punishment()
        if action == "captcha":
            return await self._handle_captcha_punishment()

        mapping = {"ban": Punishments.BAN, "kick": Punishments.KICK, "nothing": None}

        try:
            db_action = mapping[action]
        except KeyError:
            raise RuntimeError(f"No punishment found for action {action}.")

        self.settings[ViolationType[self.query.violation_type].value].type = db_action
        await self.chat.commit()

        await self.event.answer(
            f"✅ OK, now I will {punishment_set_display_text[action]} the users {settings_changed_value_display_name[self.query.violation_type]}"
        )

    async def _handle_mute_punishment(self):
        violation_type = self.query.violation_type

        return await EditMessageText(
            text=f"🔇 How long should I mute for when *{settings_description_display_name[violation_type]}*?",
            chat_id=self.event.message.chat.id,
            message_id=self.event.message.message_id,
            parse_mode="Markdown",
            reply_markup=make_mute_time_selection_keyboard(violation_type),
        )

    async def _handle_captcha_punishment(self):
        violation_type = self.query.violation_type

        return await EditMessageText(
            text=f"🔡 What type of captcha should I show when *{settings_description_display_name[violation_type]}*?",
            chat_id=self.event.message.chat.id,
            message_id=self.event.message.message_id,
            parse_mode="Markdown",
            reply_markup=make_captcha_type_selection_keyboard(violation_type),
        )


@router.callback_query(lambda q: q.data == "CreationDateSettings")
class CreationDateSettingsHandler(AdvancedCallbackQueryHandler):
    async def post_handle(self):
        keyboard = make_creation_date_selection_keyboard()
        await EditMessageText(
            text="📅 How recent should the user's account creation date be to trigger *Creation date* violation?",
            chat_id=self.event.message.chat.id,
            message_id=self.event.message.message_id,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )


class CreationDateSelectedQueryData(BaseModel):
    setting: Literal["creationdate"]
    days: int


@router.callback_query(matches_model(CreationDateSelectedQueryData))
class CreationDateSelectedHandler(AdvancedCallbackQueryHandler):
    query_model = CreationDateSelectedQueryData

    async def post_handle(self):
        self.settings.account_creation_date_less_than_months = self.query.days
        await self.chat.commit()

        await self.event.answer(
            f"✅ OK, now a creation date more recent than {self.query.days} months will trigger the violation"
        )
