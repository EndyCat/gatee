import os
from typing import List

EMOJI_CDN = os.getenv("EMOJI_CDN")


def neutralize_emoji(character: str) -> str:
    """
    Remove skin tone and gender modifiers from the emoji.
    """
    return (
        character.replace("🏻", "")
        .replace("🏼", "")
        .replace("🏽", "")
        .replace("🏾", "")
        .replace("🏿", "")
        .replace("♂️", "")
        .replace("♀️", "")
    )


def codepoint(codes: List[str]) -> str:
    # See https://github.com/twitter/twemoji/issues/419#issuecomment-637360325
    if "200d" not in codes:
        return "-".join([c for c in codes if c != "fe0f"])
    return "-".join(codes)


def get_emoji_url(character: str) -> str:
    return EMOJI_CDN + "{codepoint}.png".format(
        codepoint=codepoint(["{cp:x}".format(cp=ord(c)) for c in character])
    )
