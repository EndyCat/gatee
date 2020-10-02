"""
Adds Intellivoid spam protection support
"""
name = "20201001111916_intellivoid"
dependencies = []


def upgrade(db: "pymongo.database.Database"):
    db.chats.update_many({}, {"$set": {"settings.intellivoid_banned": {"type": None}}})


def downgrade(db: "pymongo.database.Database"):
    db.chats.update_many({}, {"$unset": {"settings.intellivoid_banned": ""}})
