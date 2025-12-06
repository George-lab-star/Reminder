from datetime import datetime

from src.celery_app import celery_app
from src.domain.entities import Reminder
from src.domain.interfaces.repositories import IUnitOfWork


async def create_reminder(
    uow: IUnitOfWork,
    user_id: int,
    text: str,
    target_time: str
) -> Reminder:
    async with uow:
        user = await uow.users.get_by_id(user_id)
        if not user:
            raise ValueError(f"!Пользователь с ID {user_id} не найден")

        reminder = Reminder(user_id=user_id, text=text, target_time=datetime.fromisoformat(target_time))
        saved_reminder = await uow.reminders.save(reminder)
        await uow.commit()
        
        return saved_reminder
