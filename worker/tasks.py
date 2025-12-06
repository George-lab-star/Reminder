import asyncio
import os
from typing import Optional

import aiohttp
from celery import Celery
from aiogram import Bot


celery = Celery(broker="redis://redis:6379/0", backend="redis://redis:6379/0")

celery.conf.update(
    worker_pool='solo',  # Обязательный параметр для async-задач
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)


@celery.task(name="hello")
def send_telegram_reminder(reminder_id: int) -> Optional[bool]:
    asyncio.run(task(reminder_id))

async def task(reminder_id: int):
    API_URL = "http://api:8000/reminders/{reminder_id}"
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL.format(reminder_id=reminder_id)) as resp:
                if resp.status != 200:
                    return False
                reminder = await resp.json()

        if reminder["is_sent"]:
            return False
        
        if not BOT_TOKEN:
            return None
        
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(
            chat_id=reminder["user_id"],
            text=f"!⏰ {reminder['text']}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.patch(
                API_URL.format(reminder_id=reminder_id),
                json={"is_sent": True}
            ) as resp:
                return resp.status == 200

    except Exception as e:
        print("f!Ошибка отправки напоминания {reminder_id}: {e}")
        raise
