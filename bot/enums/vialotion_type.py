import enum
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Punishment:
    type: int
    name: str
    db_name: str = ""

    def __post_init__(self):
        self.db_name = ViolationType[self.name].value


class ViolationType(enum.Enum):
    SpamWatchBan = "spamwatch_banned"
    CasBanned = "cas_banned"
    InappropriateAccountCreationDate = "inappropriate_account_creation_date"
    URLInName = "url_in_name"
    RTLCharactersInName = "rtl_characters_in_name"
