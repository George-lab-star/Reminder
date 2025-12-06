from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ReminderCreateRequest(BaseModel):
    user_id: int
    text: str
    target_time: str

    def to_data(self):
        """Конвертирует DTO в запрос для use‑case"""
        return {
            "user_id": self.user_id,
            "text": self.text,
            "target_time": self.target_time
        }

class ReminderUpdateRequest(BaseModel):
    text: Optional[str] = None
    target_time: Optional[str] = None
    is_sent: Optional[bool] = None

class ReminderResponse(BaseModel):
    id: int
    user_id: int
    text: str
    target_time: datetime
    is_sent: bool

    @classmethod
    def from_entity(cls, entity):
        """Создаёт ответ из сущности domain"""
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            text=entity.text,
            target_time=entity.target_time,
            is_sent=entity.is_sent
        )

class UserResponse(BaseModel):
    indoor_id: int
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @classmethod
    def from_entity(cls, entity):
        return cls(
            indoor_id=entity.indoor_id,
            id=entity.id,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name
        )

class UserCreateRequest(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
