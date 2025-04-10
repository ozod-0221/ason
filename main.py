# main.py
import asyncio
from aiogram import Bot, Dispatcher
from config import *
from database.db import async_session, init_db
from handlers.admin import admin_router
from handlers.user import user_router
from handlers.start import start_router
import logging


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    await init_db()
    # Routerlarni ulash
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)

    # Botni ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi.")
