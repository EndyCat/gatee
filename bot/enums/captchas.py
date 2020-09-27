import enum


class Captchas(enum.IntEnum):
    SIMPLE = 0
    EMOJI = 1
    RECAPTCHA = 2
