from typing import Optional

from src.domain.entities import User
from src.domain.interfaces.repositories import IUnitOfWork


async def get_user_by_id(
    uow: IUnitOfWork,
    user_id: int
) -> Optional[User]:
    async with uow:
        user = await uow.users.get_by_id(user_id)
    
    return user
