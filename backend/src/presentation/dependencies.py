from typing import Annotated

from fastapi import Depends

from src.domain.interfaces.repositories import IUnitOfWork
from src.infrastructure.db.uow import AsyncUnitOfWork


def get_uow() -> IUnitOfWork:
    return AsyncUnitOfWork()

UoWDep = Annotated[IUnitOfWork, Depends(get_uow)]
