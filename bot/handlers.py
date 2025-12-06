from datetime import datetime, timedelta

from aiogram import Router, types, F
from aiogram.filters import Command

from services import create_reminder, create_user, update_reminder


router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    if not message.from_user:
        return None
    res = await create_user(message.from_user.id, message.from_user.first_name)
    await message.answer(str(res))

@router.message(Command("remind"))
async def cmd_remind(message: types.Message):
    if not message.text:
        return None
    args = message.text.split()[1:]
    if len(args) < 2:
        await message.answer("Формат: /remind <текст> <через N минут>")
        return

    text = args[0]
    try:
        minutes = int(args[1])
    except ValueError:
        await message.answer("Укажите число минут.")
        return

    target_time = datetime.utcnow() + timedelta(minutes=minutes)

    try:
        if not message.from_user:
            return None
        if not message.from_user.id:
            return None
        reminder_id = await create_reminder(
            user_id=message.from_user.id,
            text=text,
            target_time=target_time.isoformat()
        )
        await message.answer(f"Напоминание #{reminder_id} создано!")
    except Exception as e:
        await message.answer(f"!Ошибка: {e}")

@router.message(Command("done"))
async def cmd_done(message: types.Message):
    if not message.text:
        return None
    args = message.text.split()[1:]
    if len(args) != 1:
        await message.answer("Формат: /done <ID напоминания>")
        return

    try:
        reminder_id = int(args[0])
        success = await update_reminder(reminder_id, is_sent=True)
        if success:
            await message.answer(f"Напоминание #{reminder_id} отмечено как выполненное.")
        else:
            await message.answer(f"Не удалось отметить напоминание #{reminder_id}.")
    except Exception as e:
        await message.answer(f"!Ошибка: {e}")
