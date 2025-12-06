from unittest.mock import AsyncMock

import pytest

from src.use_cases.create_user import create_user  # Ваш модуль
from src.domain.entities import User

class TestCreateUser:

    @pytest.mark.asyncio
    async def test_create_user_success(self, mock_uow):
        """Тест: пользователь успешно сохраняется."""
        # Настраиваем мок
        mock_uow.users.save = AsyncMock(return_value=User(1, "bot", "Alice", "Smith"))

        # Вызов функции
        user = await create_user(
            uow=mock_uow,
            id=1,
            username="bot",
            first_name="Alice",
            last_name="Smith"
        )

        # Проверки
        assert user.id == 1
        assert user.username == "bot"
        assert user.first_name == "Alice"
        assert user.last_name == "Smith"

        # Убедимся, что вызовы были
        mock_uow.users.save.assert_called_once()
        mock_uow.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_create_user_with_none_values(self, mock_uow):
        """Тест: поддержка None в полях."""
        mock_uow.users.save = AsyncMock(return_value=User(2, None, "Bob", None))

        user = await create_user(
            uow=mock_uow,
            id=2,
            first_name="Bob"
        )

        assert user.username is None
        assert user.last_name is None
