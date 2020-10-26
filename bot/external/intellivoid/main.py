from aiohttp import ClientResponse, ClientSession

from .. import BaseAPI
from .types import User
from typing import Optional


class Intellivoid(BaseAPI):
    BASE_URL = "https://api.intellivoid.net/spamprotection/v1/"

    def __init__(self) -> None:
        self.client = ClientSession()

    async def check(self, user_id: int) -> Optional[User]:
        async with self.client.get(
            self.BASE_URL + "lookup", params={"query": user_id}
        ) as response:  # type: ClientResponse
            json_response = await response.json(content_type=None)

            if "error" in json_response:
                return None

            return User(**json_response["results"])
