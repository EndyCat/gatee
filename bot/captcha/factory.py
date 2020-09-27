from ..enums import Captchas
from . import EmojiCaptchaSender, ReCaptchaSender, SimpleCaptchaSender


def make_captcha_sender(captcha_type: int):
    mapping = {
        Captchas.SIMPLE: SimpleCaptchaSender,
        Captchas.EMOJI: EmojiCaptchaSender,
        Captchas.RECAPTCHA: ReCaptchaSender,
    }

    try:
        return mapping[captcha_type]  # noqa
    except KeyError:
        raise RuntimeError(f"No captcha sender found for captcha type {captcha_type}.")
