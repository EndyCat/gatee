import os
import random
from dataclasses import dataclass
from io import BytesIO
from typing import Any, List, Tuple

import emoji
from aiocache import cached
from aiogram.api.methods import SendPhoto
from aiogram.api.types import (
    BufferedInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiohttp import ClientSession
from PIL import Image, ImageDraw, UnidentifiedImageError

from ..utils.emoji import get_emoji_url, neutralize_emoji
from ..utils.misc import interpolate
from ..utils.telegram import mention
from . import BaseCaptchaSender


@dataclass
class EmojiSequence:
    correct_emoji: str
    other_emojis: List[str]


@dataclass
class EmojiCaptchaChallenge:
    image: Any
    emoji_sequence: EmojiSequence


class EmojiCaptchaSender(BaseCaptchaSender):
    gradient_colors = [
        (253, 227, 170),
        (238, 186, 223),
        (174, 181, 231),
        (187, 230, 225),
        (144, 209, 225),
        (242, 230, 224),
    ]

    emojis = list(emoji.UNICODE_EMOJI)
    short_emojis = list(filter(lambda e: len(e) <= 2, emojis))

    async def send(self, challenge):
        emoji_challenge = await self.make_emoji_image()

        challenge.correct_emoji_answer = emoji_challenge.emoji_sequence.correct_emoji
        await challenge.commit()

        image_bytesio = BytesIO()
        emoji_challenge.image.save(image_bytesio, format="PNG")
        image_bytesio_value = image_bytesio.getvalue()

        buttons = [
            [
                InlineKeyboardButton(
                    text=variant,
                    callback_data=f"captcha_emoji_{challenge.uuid}_{variant}",
                )
                for variant in emoji_challenge.emoji_sequence.other_emojis
            ]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        return await SendPhoto(
            chat_id=self.chat.id,
            photo=BufferedInputFile(file=image_bytesio_value, filename="captcha.png"),
            caption=f"🤖 {mention(self.user)}, please select the *matching* emoji!",
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

    async def make_emoji_image(self) -> EmojiCaptchaChallenge:
        f_co, t_co = (
            random.choice(self.gradient_colors),
            random.choice(self.gradient_colors),
        )
        width, height = map(int, os.getenv("EMOJI_CAPTCHA_IMAGE_SIZE").split("x"))
        image = self._make_gradient_image((width, height), f_co, t_co)

        while True:
            try:
                emoji_sequence = self._make_random_emoji_sequence()
                correct_emoji_image = await self._get_emoji_image(
                    emoji_sequence.correct_emoji
                )
                break
            except UnidentifiedImageError:  # Sometimes it may return 404 instead of emojis
                pass

        img_w, img_h = image.size
        emoji_w, emoji_h = correct_emoji_image.size

        offset = ((img_w - emoji_w) // 2, (img_h - emoji_h) // 2)

        image.paste(correct_emoji_image, offset, correct_emoji_image.convert("RGBA"))

        return EmojiCaptchaChallenge(image, emoji_sequence)

    def _make_random_emoji_sequence(self, emojis: List[str] = None) -> EmojiSequence:
        if emojis is None:
            emojis = self.short_emojis

        correct_emoji = neutralize_emoji((random.choice(emojis)))

        other_emojis = random.choices(emojis, k=2) + [correct_emoji]
        other_emojis = [neutralize_emoji(e) for e in other_emojis]
        random.shuffle(other_emojis)

        return EmojiSequence(correct_emoji, other_emojis)

    @staticmethod
    @cached(ttl=300)
    async def _get_emoji_image(character: str) -> Image:
        async with ClientSession() as session:
            response = await session.get(get_emoji_url(character))
            return Image.open(BytesIO(await response.content.read()))

    @staticmethod
    def _make_gradient_image(
        size: Tuple[int, int], f_co: Tuple[int, int, int], t_co: Tuple[int, int, int]
    ):
        image = Image.new("RGBA", size)
        draw = ImageDraw.Draw(image)

        for i, color in enumerate(interpolate(f_co, t_co, image.width * 2)):
            draw.line([(i, 0), (0, i)], tuple(color), width=1)

        return image
