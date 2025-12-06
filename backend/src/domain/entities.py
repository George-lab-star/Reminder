from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Reminder:
    user_id: int
    text: str
    target_time: datetime
    id: Optional[int] = None
    is_sent: bool = False

@dataclass
class User:
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    indoor_id: Optional[int] = None
