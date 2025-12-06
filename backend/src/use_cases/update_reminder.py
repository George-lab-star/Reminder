from typing import Optional
from datetime import datetime

from fastapi import HTTPException

from src.domain.interfaces.repositories import IUnitOfWork
from src.domain.entities import Reminder


async def update_reminder(
    uow: IUnitOfWork,
    reminder_id: int,
    text: Optional[str] = None,
    target_time: Optional[str] = None,
    is_sent: Optional[bool] = None
) -> Optional[Reminder]:
    async with uow:
        reminder = await uow.reminders.get_by_id(reminder_id)
        if not reminder:
            raise HTTPException(
                status_code=404,
                detail=f"Напоминание с ID {reminder_id} не найдено"
            )

        if text is not None:
            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Текст напоминания не может быть пустым"
                )
            reminder.text = text.strip()

        if target_time is not None:
            reminder.target_time = datetime.fromisoformat(target_time)

        if is_sent is not None:
            reminder.is_sent = is_sent

        updated_reminder = await uow.reminders.update(reminder)
        await uow.commit()

        return updated_reminder
