from unittest.mock import AsyncMock

import pytest

from src.domain.entities import User
from src.use_cases.get_user_by_id import get_user_by_id


class TestGetUserById:

    @pytest.mark.asyncio
    async def test_get_user_found(self, mock_uow):
        """Тест: пользователь найден."""
        expected_user = User(1, "user1", "John", "Doe")
        mock_uow.users.get_by_id = AsyncMock(return_value=expected_user)

        user = await get_user_by_id(mock_uow, 1)

        assert user == expected_user
        mock_uow.users.get_by_id.assert_awaited_with(1)
    
    @pytest.mark.asyncio
    async def test_get_user_not_found(self, mock_uow):
        """Тест: пользователь не найден (возвращает None)."""
        mock_uow.users.get_by_id = AsyncMock(return_value=None)

        user = await get_user_by_id(mock_uow, 999)

        assert user is None
        mock_uow.users.get_by_id.assert_awaited_with(999)
