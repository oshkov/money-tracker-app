from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.database import get_async_session
from src.auth.schemas import UserRead
from src.auth.utils import get_current_user


router = APIRouter(
    tags=['Operations']
)


@router.post('/create-operation')
async def create_operation(
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    return user