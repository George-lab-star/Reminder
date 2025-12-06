from fastapi import APIRouter, Depends, HTTPException

from src.domain.dtos import ReminderCreateRequest, ReminderResponse, ReminderUpdateRequest
from src.use_cases.create_reminder import create_reminder
from src.use_cases.update_reminder import update_reminder
from src.presentation.dependencies import UoWDep
from src.celery_app import celery_app


router = APIRouter(prefix="/reminders", tags=["reminders"])

@router.post("/",
    response_model=ReminderResponse,
    status_code=201
)
async def create_reminder_endpoint(
    request: ReminderCreateRequest,
    uow: UoWDep
):
    try:
        reminder = await create_reminder(uow, request.user_id, request.text, request.target_time)
        celery_app.send_task(
            "hello",           # имя задачи (строка!)
            args=[reminder.id],                # аргументы
            eta=reminder.target_time         # время выполнения
        )
        return ReminderResponse.from_entity(reminder)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/{reminder_id}", response_model=ReminderResponse)
async def get_reminder(
    reminder_id: int,
    uow: UoWDep
):
    async with uow:
        reminder = await uow.reminders.get_by_id(reminder_id)
        if not reminder:
            raise HTTPException(status_code=404, detail="Напоминание не найдено")
        return ReminderResponse.from_entity(reminder)

@router.patch("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder_endpoint(
    reminder_id: int,
    request: ReminderUpdateRequest,
    uow: UoWDep
):
    try:
        updated_reminder = await update_reminder(
            reminder_id=reminder_id,
            text=request.text,
            target_time=request.target_time,
            is_sent=request.is_sent,
            uow=uow
        )
        return ReminderResponse.from_entity(updated_reminder)

    except HTTPException as e:
        raise e  # Передаём HTTP‑ошибки наверх
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка сервера: {str(e)}"
        )
