from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.database import get_async_session
from src.news.utils import get_news
from src.redis import get_redis_client


router = APIRouter(
    tags=['News']
)

@router.get('/get-news')
async def get_accounts_route(
    session = Depends(get_async_session),
    redis = Depends(get_redis_client)
):
    try:
        # Получение новостей
        news = await get_news(session, redis)

        response_data = {
            'status': 'success',
            'data': news,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)
    
    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)