import uuid as uuid_
from typing import NoReturn, Optional, Union

import umongo
from umongo import fields

from ..db import Instance

instance: umongo.Instance = Instance.get_current().instance


@instance.register
class CaptchaChallenge(umongo.Document):
    uuid = fields.StringField(required=True)
    chat_id = fields.IntegerField(required=True)
    user_id = fields.IntegerField(required=True)
    message_id = fields.IntegerField(
        required=True, allow_none=True
    )  # Message to delete after the captcha is solved

    correct_emoji_answer = fields.StringField()  # Only used for emoji captcha

    class Meta:
        collection_name = "challenges"

    @staticmethod
    async def create_challenge(
        chat_id: int, user_id: int, message_id: Optional[int]
    ) -> Union["CaptchaChallenge", NoReturn]:
        existing_challenge = await CaptchaChallenge.find_one(
            {"chat_id": chat_id, "user_id": user_id}
        )

        if existing_challenge:
            await existing_challenge.delete()

        challenge = CaptchaChallenge(
            uuid=str(uuid_.uuid4()),
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
        )
        await challenge.commit()
        return challenge

    @staticmethod
    async def get_challenge(uuid: str) -> Optional["CaptchaChallenge"]:
        challenge = await CaptchaChallenge.find_one({"uuid": uuid})
        return challenge
