from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


router = APIRouter(
    tags=['Theme']
)

@router.post('/switch-theme')
async def switch_theme(request: Request):
    try:
        # Получение темы из куки
        theme = request.cookies.get('theme')

        if theme == 'light' or theme == None:
            new_theme = 'dark'
        elif theme == 'dark':
            new_theme = 'light'

        response_data = {
            'status': 'success',
            'data': new_theme,
            'detail': None
        }

        response = JSONResponse(content=response_data, status_code=200)

        # Добавление темы в куки
        response.set_cookie(key='theme', value=new_theme)

        return response

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)