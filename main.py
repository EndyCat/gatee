import asyncio
import logging
import os

import uvicorn
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.utils.telegram import include_routers

load_dotenv()

from bot.web.main import app


def main():
    logging.basicConfig(level=os.getenv("LOGGING_LEVEL"))

    @app.on_event("startup")
    async def on_startup():
        bot = Bot(token=os.getenv("API_TOKEN"), parse_mode="Markdown")
        Bot.set_current(bot)
        dp = Dispatcher()

        loop = asyncio.get_event_loop()

        include_routers(dp)
        app.state.bot = bot

        loop.create_task(dp.start_polling(bot))

    uvicorn.run(
        app, host=os.getenv("WEB_SERVER_HOST"), port=int(os.getenv("WEB_SERVER_PORT"))
    )


if __name__ == "__main__":
    main()
