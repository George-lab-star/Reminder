from src.domain.interfaces.repositories import IUnitOfWork


async def send_reminder(
    uow: IUnitOfWork,
    reminder_id: int
) -> bool:
    async with uow:
        reminder = await uow.reminders.get_by_id(reminder_id)
        if not reminder or reminder.is_sent:
            return False

        reminder.is_sent = True
        await uow.reminders.update(reminder)
        await uow.commit()
    return True
