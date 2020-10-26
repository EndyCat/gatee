from aiohttp import ClientResponse, ClientSession

from .. import BaseAPI
from .types import Ban
from typing import Optional


class SpamWatch(BaseAPI):
    BASE_URL = "https://api.spamwat.ch/"

    def __init__(self, api_key: str):
        self.client = ClientSession(
            headers={"Authorization": f"Bearer {api_key}"},
        )

    async def check(self, user_id: int) -> Optional[Ban]:
        async with self.client.get(
            self.BASE_URL + f"banlist/{user_id}"
        ) as response:  # type: ClientResponse
            json_response = await response.json(content_type=None)

            if "error" in json_response:
                return None
            return Ban(**json_response)
