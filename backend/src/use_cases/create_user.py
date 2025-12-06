from typing import Optional

from src.domain.entities import User
from src.domain.interfaces.repositories import IUnitOfWork


async def create_user(
    uow: IUnitOfWork,
    id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
):
    user = User(id, username, first_name, last_name)
    async with uow:
        user = await uow.users.save(user)
        await uow.commit()
        return user
