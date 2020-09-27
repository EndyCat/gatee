from ..enums import Punishments

punishments_main_menu_display_name = {
    Punishments.BAN: "ban",
    Punishments.KICK: "kick",
    Punishments.MUTE: "mute",
    Punishments.CAPTCHA: "captcha",
    None: "nothing",
}

punishments_selection_menu_display_name = {
    "🔪 Ban": "ban",
    "🔫 Kick": "kick",
    "🔇 Mute": "mute",
    "🔡 Captcha": "captcha",
    "Nothing": "nothing",
}

violations_display_name = {
    "InappropriateAccountCreationDate": "Creation 📅",
    "URLInName": "URL 🔗",
    "SpamWatchBan": "SpamWatch ⛔️",
    "CasBanned": "CAS ⛔️",
    "RTLCharactersInName": "RTL 🈴",
}

settings_description_display_name = {
    "SpamWatchBan": "the user is SpamWatch banned",
    "CasBanned": "the user is CAS banned",
    "InappropriateAccountCreationDate": "user's account creation date is too recent",
    "URLInName": "the user has URL in name",
    "RTLCharactersInName": "the user has RTL characters in name (including all RTL languages)",
}

settings_changed_value_display_name = {
    "SpamWatchBan": "that are SpamWatch banned",
    "CasBanned": "that are CAS banned",
    "InappropriateAccountCreationDate": "who's account creation date is too recent",
    "URLInName": "that have URL in name",
    "RTLCharactersInName": "that have RTL characters in name (including all RTL languages)",
}

punishment_set_display_text = {
    "ban": "ban",
    "kick": "kick",
    "nothing": "do nothing about",
}
