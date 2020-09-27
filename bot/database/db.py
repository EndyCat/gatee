import asyncio
import contextvars
import os
from typing import Type, TypeVar

import umongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

T = TypeVar("T")


class ContextInstanceMixin:
    def __init_subclass__(cls, **_):
        cls.__context_instance = contextvars.ContextVar("instance_" + cls.__name__)
        return cls

    @classmethod
    def get_current(cls: Type[T], no_error=True) -> T:
        if no_error:
            return cls.__context_instance.get(None)
        return cls.__context_instance.get()

    @classmethod
    def set_current(cls: Type[T], value: T):
        if not isinstance(value, cls):
            raise TypeError(
                f"Value should be instance of '{cls.__name__}' not '{type(value).__name__}'"
            )
        cls.__context_instance.set(value)


class DB(ContextInstanceMixin):
    def __init__(self):
        self.client = AsyncIOMotorClient(host=os.getenv("MONGODB_HOST"))
        self.db = self.client["gatee"]

        AsyncIOMotorCollection.get_io_loop = (
            lambda _: asyncio.get_event_loop()
        )  # Make AsyncIOMotorCollection use asyncio event loop

        self.set_current(self)


class Instance(ContextInstanceMixin):
    """
    uMongo DB instance.
    """

    def __init__(self, db_: DB = None):
        if not db_:
            self.db = DB.get_current().db
        else:
            self.db = db_

        self.instance = umongo.Instance(self.db)

        self.set_current(self)


db = DB()
instance = Instance()
