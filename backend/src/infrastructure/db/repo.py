from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.domain.interfaces.repositories import IReminderRepository, IUserRepository
from src.infrastructure.db.models import ReminderModel, UserModel
from src.domain.entities import Reminder, User


class AsyncReminderRepository(IReminderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, reminder: Reminder) -> Reminder:
        model = ReminderModel(
            user_id=reminder.user_id,
            text=reminder.text,
            target_time=reminder.target_time,
            is_sent=reminder.is_sent
        )
        self.session.add(model)
        await self.session.flush()
        reminder.id = model.id
        return reminder

    async def get_by_user(self, user_id: int) -> list[Reminder]:
        result = await self.session.execute(
            select(ReminderModel).where(ReminderModel.user_id == user_id)
        )
        models = result.scalars().all()
        return [
            Reminder(
                id=model.id,
                user_id=model.user_id,
                text=model.text,
                target_time=model.target_time,
                is_sent=model.is_sent
            ) for model in models
        ]

    async def get_by_id(self, id: int) -> Optional[Reminder]:
        result = await self.session.execute(
            select(ReminderModel).where(ReminderModel.id == id)
        )
        model = result.scalar()
        if not model:
            return None
        return self._to_entity(model)

    async def update(self, reminder: Reminder) -> Optional[Reminder]:
        updated_reminder = await self.session.execute(
            update(ReminderModel)
            .where(ReminderModel.id == reminder.id)
            .values(is_sent=reminder.is_sent)
            .returning(ReminderModel)
        )
        await self.session.flush()
        updated_reminder = await self.session.execute(
            select(ReminderModel).where(ReminderModel.id == id)
        )
        updated_reminder = updated_reminder.scalar()
        if not updated_reminder:
            return None
        return self._to_entity(updated_reminder)
    
    def _to_entity(self, model: ReminderModel) -> Reminder:
        return Reminder(
            user_id=model.user_id,
            text=model.text,
            target_time=model.target_time,
            id=model.id
        )


class AsyncUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        self.session.add(model)
        await self.session.flush()
        return self._to_entity(model)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar()
        if not model:
            return None
        return self._to_entity(model)
    
    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            indoor_id=model.indoor_id
        )
    