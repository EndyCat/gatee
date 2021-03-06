import os
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Awaitable, Optional, Union

from aiogram.api.types import User

from .database.models import ChatSettings
from .enums import ViolationType
from .external import CAS, CreationDate, Intellivoid, SpamWatch
from .external.cas.types import User as CASUser
from .external.spamwatch.types import Ban
from .regex import rtl_re, url_re


class ViolationDetector(ABC):
    @abstractmethod
    def is_detected(
        self, user: User, settings: ChatSettings
    ) -> Union[Awaitable[bool], bool]:
        raise NotImplementedError


class SpamWatchBanDetector(ViolationDetector):
    async def is_detected(self, user: User, settings: ChatSettings) -> bool:
        return await self._find_spamwatch_ban(user) is not None

    @staticmethod
    async def _find_spamwatch_ban(user: User) -> Optional[Ban]:
        async with SpamWatch(os.getenv("SPAMWATCH_TOKEN")) as spamwatch:
            spamwatch_check = await spamwatch.check(user.id)
            return spamwatch_check


class CasBanDetector(ViolationDetector):
    async def is_detected(self, user: User, settings: ChatSettings) -> bool:
        return await self._find_cas_ban(user) is not None

    @staticmethod
    async def _find_cas_ban(user: User) -> Optional[CASUser]:
        async with CAS() as cas:
            cas_check = await cas.check(user.id)
            return cas_check


class IntellivoidBanDetector(ViolationDetector):
    async def is_detected(self, user: User, settings: ChatSettings) -> bool:
        return await self._check_intellivoid_ban(user)

    @staticmethod
    async def _check_intellivoid_ban(user: User) -> bool:
        async with Intellivoid() as intellivoid:
            intellivoid_check = await intellivoid.check(user.id)

        return intellivoid_check is not None and intellivoid_check.attributes is not None


class InappropriateAccountCreationDateDetector(ViolationDetector):
    def is_detected(self, user: User, settings: ChatSettings) -> bool:
        time_since_creation = datetime.now() - self._get_creation_datetime(user=user)
        return (
            time_since_creation.days
            < settings.account_creation_date_less_than_months * 30
        )

    @staticmethod
    def _get_creation_datetime(user: User) -> datetime:
        created_at = CreationDate().get_creation_date(user.id)
        return datetime.utcfromtimestamp(created_at)


class URLInNameDetector(ViolationDetector):
    def is_detected(self, user: User, settings: ChatSettings) -> bool:
        name = f"{user.first_name} {user.last_name}"
        return bool(re.search(url_re, name))


class RTLCharactersInNameDetector(ViolationDetector):
    def is_detected(self, user: User, settings: ChatSettings) -> bool:
        name = f"{user.first_name} {user.last_name}"
        return bool(re.search(rtl_re, name))


def make_violation_detector(violation_type: ViolationType) -> ViolationDetector:
    mapping = {
        ViolationType.SpamWatchBan: SpamWatchBanDetector,
        ViolationType.CasBanned: CasBanDetector,
        ViolationType.InappropriateAccountCreationDate: InappropriateAccountCreationDateDetector,
        ViolationType.URLInName: URLInNameDetector,
        ViolationType.RTLCharactersInName: RTLCharactersInNameDetector,
        ViolationType.IntellivoidBan: IntellivoidBanDetector,
    }
    try:
        return mapping[violation_type]()
    except KeyError:
        raise RuntimeError(
            f"No violation detector found for violation type {violation_type!r}."
        )
