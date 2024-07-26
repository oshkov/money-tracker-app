from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.database import get_async_session
from src.auth.utils import create_user, verify_password, create_access_token, get_user_by_email
from src.auth.schemas import UserCreate, UserLogin


router = APIRouter(
    tags=['Auth']
)


@router.post('/register')
async def register(
    user: UserCreate,
    session = Depends(get_async_session)
):
    try:
        user_in_db = await get_user_by_email(session, user.email)
        if user_in_db:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'User already registered'
            }
            return JSONResponse(content=response_data, status_code=409)

        await create_user(session, user)

        jwt_token = await create_access_token(session, user.email)

        response_data = {
                'status': 'success',
                'data': {
                    'jwt_token': jwt_token,
                    'token_type': 'jwt_token'
                },
                'detail': None
            }
        response = JSONResponse(content=response_data, status_code=200)
        response.set_cookie(key='jwt_token', value=jwt_token, max_age=3600)

        return response

    except Exception as error:
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)
    

@router.post('/login')
async def login(
    user: UserLogin,
    session = Depends(get_async_session)
):
    try:
        # Проверка пароля пользователя
        if await verify_password(session, user.email, user.password):
            
            # Создание JWT токена
            jwt_token = await create_access_token(session, user.email)

            response_data = {
                'status': 'success',
                'data': {
                    'jwt_token': jwt_token,
                    'token_type': 'jwt_token'
                },
                'detail': None
            }
            response = JSONResponse(content=response_data, status_code=200)

            # Добавление токена в куки
            response.set_cookie(key='jwt_token', value=jwt_token, max_age=3600)

            return response
        
        # Ошибка авторизации
        else:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Invalid credentials'
            }
            return JSONResponse(content=response_data, status_code=400)

    # Ошибка сервера
    except Exception as error:
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)
    

@router.post('/logout')
async def logout():
    try:
        response_data = {
            'status': 'success',
            'data': None,
            'detail': None
        }
        response = JSONResponse(content=response_data)
        response.delete_cookie('jwt_token')

        return response

    except Exception as error:
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)