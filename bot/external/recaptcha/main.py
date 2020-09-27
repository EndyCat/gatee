from typing import Optional

from aiohttp import ClientResponse, ClientSession

from .. import BaseAPI
from .types import ReCaptchaResponse


class ReCaptcha(BaseAPI):
    BASE_URL = "https://www.google.com/recaptcha/api/"

    def __init__(self, secret: str):
        self.secret = secret
        self.client = ClientSession()

    async def verify(self, response: str, remoteip: Optional[str] = None):
        data = {"secret": self.secret, "response": response}
        if remoteip is not None:
            data["remoteip"] = remoteip

        async with self.client.post(
            self.BASE_URL + "siteverify", data=data
        ) as response:  # type: ClientResponse
            json_response = await response.json()

            return ReCaptchaResponse(**json_response)
