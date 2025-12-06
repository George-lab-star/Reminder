from typing import List, Optional, Self
from abc import ABC, abstractmethod

from src.domain.entities import Reminder, User


class IReminderRepository(ABC):
    @abstractmethod
    async def save(self, reminder: Reminder) -> Reminder:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int) -> List[Reminder]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Reminder]:
        pass

    @abstractmethod
    async def update(self, reminder: Reminder) -> Optional[Reminder]:
        pass


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

class IUnitOfWork(ABC):
    reminders: IReminderRepository
    users: IUserRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
