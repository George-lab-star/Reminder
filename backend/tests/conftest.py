import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_uow():
    """Создаёт мокнутый UoW с репозиториями."""
    uow = MagicMock()

    # Мокируем репозитории
    uow.users = MagicMock()
    uow.reminders = MagicMock()

    # AsyncContextManager для `async with uow`
    class AsyncContextManager:
        async def __aenter__(self):
            return uow
        async def __aexit__(self, exc_type, exc, tb):
            pass

    uow.__aenter__ = AsyncContextManager().__aenter__
    uow.__aexit__ = AsyncContextManager().__aexit__

    return uow
