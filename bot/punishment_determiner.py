import inspect
from typing import Optional

from aiogram.api.types import User

from .database.models import ChatSettings
from .enums import Punishment, ViolationType
from .violation_detector import make_violation_detector


async def determine_punishment(
    user: User, settings: ChatSettings
) -> Optional[Punishment]:
    for punishment in settings.sort_punishments_by_weight():
        violation_type = ViolationType[punishment.name]
        violation_detector = make_violation_detector(violation_type)

        is_detected = violation_detector.is_detected

        if inspect.iscoroutinefunction(is_detected):
            is_violation_detected = await is_detected(user=user, settings=settings)
        else:
            is_violation_detected = is_detected(user=user, settings=settings)

        if is_violation_detected:
            return punishment
