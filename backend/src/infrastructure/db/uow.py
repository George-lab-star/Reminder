from src.domain.interfaces.repositories import IUnitOfWork
from src.infrastructure.db.engine import async_session_maker
from src.infrastructure.db.repo import AsyncReminderRepository, AsyncUserRepository


class AsyncUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory=async_session_maker):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.reminders = AsyncReminderRepository(self.session)
        self.users = AsyncUserRepository(self.session)
        return self

    async def __aexit__(self, type, value, traceback):
        if type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
