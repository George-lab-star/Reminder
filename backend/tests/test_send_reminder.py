from unittest.mock import AsyncMock, MagicMock

import pytest

from src.use_cases.send_reminder import send_reminder


class TestSendReminder:

    @pytest.mark.asyncio
    async def test_send_reminder_success(self, mock_uow):
        """Тест: напоминание отправлено (is_sent=True)."""
        reminder = MagicMock(is_sent=False)
        mock_uow.reminders.get_by_id = AsyncMock(return_value=reminder)
        mock_uow.reminders.update = AsyncMock()


        result = await send_reminder(mock_uow, 1)

        assert result is True
        assert reminder.is_sent is True
        mock_uow.reminders.update.assert_awaited_once_with(reminder)
        mock_uow.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_send_reminder_already_sent(self, mock_uow):
        """Тест: напоминание уже отправлено (возвращает False)."""
        reminder = MagicMock(is_sent=True)
        mock_uow.reminders.get_by_id = AsyncMock(return_value=reminder)

        result = await send_reminder(mock_uow, 1)

        assert result is False
        mock_uow.reminders.update.assert_not_awaited()
        mock_uow.commit.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_send_reminder_not_found(self, mock_uow):
        """Тест: напоминание не найдено (возвращает False)."""
        mock_uow.reminders.get_by_id = AsyncMock(return_value=None)

        result = await send_reminder(mock_uow, 999)

        assert result is False
        mock_uow.reminders.update.assert_not_awaited()
        mock_uow.commit.assert_not_awaited()
