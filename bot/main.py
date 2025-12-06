import asyncio
import logging

from aiogram import Bot, Dispatcher

import config, handlers


logging.basicConfig(level=logging.INFO)

async def main():
    if not config.BOT_TOKEN:
        return None
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(handlers.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
