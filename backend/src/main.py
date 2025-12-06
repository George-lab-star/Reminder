from fastapi import FastAPI

from src.infrastructure.db.models import Base
from src.infrastructure.db.engine import engine
from src.presentation.routers.reminders_router import router as reminders_router
from src.presentation.routers.users_routes import router as users_router


app = FastAPI(
    title="Reminder",
    description="""Простой, но функциональный бот, напоминающий пользователю о чём-либо..""",
)

@app.on_event("startup")
async def event_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def event_shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

app.include_router(reminders_router)

app.include_router(users_router)
