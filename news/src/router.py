from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.utils import get_news


router = APIRouter(
    tags=['News']
)

@router.get('/get-news')
async def get_accounts_route():
    try:
        # Получение новостей
        news = await get_news()

        response_data = {
            'status': 'success',
            'data': news,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)
    
    except Exception as error:
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)