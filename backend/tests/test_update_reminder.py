from datetime import datetime, timezone

from fastapi import HTTPException
import pytest

from src.use_cases.update_reminder import update_reminder
from src.domain.entities import Reminder


class TestUpdateReminderUseCase:

    @pytest.mark.asyncio
    async def test_update_text_success(self, mock_uow):
        """Тест: успешное обновление текста."""
        # Исходное напоминание
        existing_reminder = Reminder(
            id=1,
            user_id=100,
            text="Старый текст",
            target_time=datetime(2025, 12, 5, 10, 0, tzinfo=timezone.utc),
            is_sent=False
        )

        # Настраиваем мок
        mock_uow.reminders.get_by_id.return_value = existing_reminder
        mock_uow.reminders.update.return_value = existing_reminder  # после обновления

        # Вызов use case
        updated = await update_reminder(
            uow=mock_uow,
            reminder_id=1,
            text="Новый текст"
        )

        # Проверки
        assert updated.text == "Новый текст"
        assert updated.id == 1
        mock_uow.reminders.get_by_id.assert_awaited_with(1)
        mock_uow.reminders.update.assert_awaited_once()
        mock_uow.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update_target_time(self, mock_uow):
        """Тест: обновление времени."""
        existing_reminder = Reminder(
            id=2,
            user_id=101,
            text="Тест",
            target_time=datetime(2025, 12, 5, 10, 0, tzinfo=timezone.utc),
            is_sent=False
        )
        new_time = datetime(2025, 12, 6, 15, 0, tzinfo=timezone.utc)

        mock_uow.reminders.get_by_id.return_value = existing_reminder
        mock_uow.reminders.update.return_value = existing_reminder

        updated = await update_reminder(
            uow=mock_uow,
            reminder_id=2,
            target_time=new_time.isoformat()
        )

        assert updated.target_time == new_time
        mock_uow.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update_is_sent(self, mock_uow):
        """Тест: отметка как отправленное."""
        existing_reminder = Reminder(id=3, user_id=102, text="Тест", target_time=datetime.now(timezone.utc), is_sent=False)

        mock_uow.reminders.get_by_id.return_value = existing_reminder
        mock_uow.reminders.update.return_value = existing_reminder

        updated = await update_reminder(
            uow=mock_uow,
            reminder_id=3,
            is_sent=True
        )

        assert updated.is_sent is True

    @pytest.mark.asyncio
    async def test_reminder_not_found_raises_404(self, mock_uow):
        """Тест: напоминание не найдено → HTTP 404."""
        mock_uow.reminders.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await update_reminder(uow=mock_uow, reminder_id=999, text="Текст")

        assert exc_info.value.status_code == 404
        assert "Напоминание с ID 999 не найдено" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_empty_text_raises_400(self, mock_uow):
        """Тест: пустой текст → HTTP 400."""
        existing_reminder = Reminder(id=4, user_id=103, text="Было", target_time=datetime.now(timezone.utc), is_sent=False)
        mock_uow.reminders.get_by_id.return_value = existing_reminder


        with pytest.raises(HTTPException) as exc_info:
            await update_reminder(uow=mock_uow, reminder_id=4, text="   ")

        assert exc_info.value.status_code == 400
        assert "Текст напоминания не может быть пустым" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_no_fields_to_update(self, mock_uow):
        """Тест: ничего не передано → напоминание не меняется."""
        existing_reminder = Reminder(id=5, user_id=104, text="Без изменений", target_time=datetime.now(timezone.utc), is_sent=False)
        mock_uow.reminders.get_by_id.return_value = existing_reminder
        mock_uow.reminders.update.return_value = existing_reminder

        updated = await update_reminder(uow=mock_uow, reminder_id=5)

        assert updated == existing_reminder
        mock_uow.reminders.update.assert_not_awaited()  # Не вызывается, т.к. нет изменений
        mock_uow.commit.assert_not_awaited()   # Транза