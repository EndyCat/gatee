import umongo
from umongo import fields, validate

from ...utils.display import violations_display_name
from ...utils.misc import sort_punishments_by_weight
from ..db import Instance

instance: umongo.Instance = Instance.get_current().instance


@instance.register
class Punishment(umongo.EmbeddedDocument):
    type = fields.IntegerField(required=True, allow_none=True)
    mute_for = fields.IntegerField()
    captcha_type = fields.IntegerField(validate=validate.Range(0, 2))


@instance.register
class ChatSettings(umongo.EmbeddedDocument):
    cas_banned = fields.EmbeddedField(Punishment)
    spamwatch_banned = fields.EmbeddedField(Punishment)
    intellivoid_banned = fields.EmbeddedField(Punishment)
    account_creation_date_less_than_months = fields.IntegerField()
    inappropriate_account_creation_date = fields.EmbeddedField(Punishment)
    rtl_characters_in_name = fields.EmbeddedField(Punishment)
    url_in_name = fields.EmbeddedField(Punishment)

    def sort_punishments_by_weight(
        self, ignore_none_punishments: bool = True, sort_by_length: bool = False
    ):
        punishments = sort_punishments_by_weight(self, ignore_none_punishments)

        if sort_by_length:
            punishments = sorted(
                punishments, key=lambda p: len(violations_display_name[p.name])
            )

        return punishments
