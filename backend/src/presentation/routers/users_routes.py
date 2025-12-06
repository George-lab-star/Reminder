from fastapi import APIRouter, HTTPException

from src.domain.dtos import UserCreateRequest, UserResponse
from src.use_cases.create_user import create_user
from src.use_cases.get_user_by_id import get_user_by_id
from src.presentation.dependencies import UoWDep


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user_endpoint(
    request: UserCreateRequest,
    uow: UoWDep
):
    try:
        user = await create_user(
            uow=uow,
            id=request.id,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name
        )
        return UserResponse.from_entity(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    uow: UoWDep
):
    user = await get_user_by_id(uow, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_entity(user)