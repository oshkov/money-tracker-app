from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import httpx

from src.database import get_async_session
from src.schemas import (
    AccountCreate,
    AccountDelete,
    AccountEdit,
    CategoryCreate,
    CategoryDelete,
    СategoryEdit,
    OperationCreate,
    OperationDelete,
    OperationEdit
)
from src.utils import (
    create_account,
    get_account_by_title,
    delete_account,
    edit_account,
    get_category_by_title,
    create_category,
    delete_category,
    edit_category,
    create_operation,
    delete_operation,
    edit_operation,
    get_accounts,
    get_categories,
    get_operations
)


router = APIRouter(
    tags=['Tracker']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
async def login():
    return {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTEsImVtYWlsIjoiMSIsInVzZXJuYW1lIjoiXHUwNDIxXHUwNDMwXHUwNDQ4XHUwNDNhXHUwNDMwIiwic3VwZXJ1c2VyIjpmYWxzZSwiZXhwIjo1MzI2NzcxMjI5fQ.6Qp1Gc6_op698rUdmcKwbMjfE3GpAVRLWVQ6yQH8ypY", "token_type": "bearer"}


async def get_current_user(token):
    '''
    Функция запроса данных о пользователе из микросервиса с аутентификацией
    '''

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'http://185.237.165.219:8002/get-current-user',
                headers={'Authorization': f'Bearer {token}'}
            )
            user = response.json()['data']

            # Вывод ошибки если данные о пользователе не получены
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail='Auth service error')

            return user

    except Exception as error:
        raise error


@router.get('/get-accounts')
async def get_accounts_route(
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)

        # Получение счетов пользователя
        accounts = await get_accounts(session, user)

        response_data = {
            'status': 'success',
            'data': accounts,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)

    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.post('/create-account')
async def create_account_route(
    account: AccountCreate,
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)
 
        # Проверка на наличие такого счета у пользователя
        account_in_db = await get_account_by_title(session, account.title)
        if account_in_db:
            raise HTTPException(status_code=409, detail='Account already created')

        # Создание счета пользователя
        new_account = await create_account(session, user, account)

        response_data = {
            'status': 'success',
            'data': new_account,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)

    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.delete('/delete-account')
async def delete_account_route(
    account: AccountDelete,
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)

        # Удаление счета пользователя
        await delete_account(session, account)

        response_data = {
            'status': 'success',
            'data': None,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)

    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.put('/edit-account')
async def edit_account_route(
    account: AccountEdit,
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)

        # Проверка на наличие такого счета у пользователя
        # Ошибка только при разных id счетов
        account_in_db = await get_account_by_title(session, account.title)
        if account_in_db and account.id != account_in_db.account_id:
            raise HTTPException(status_code=409, detail='Account already created')

        # Изменение счета пользователя
        await edit_account(session, account)

        response_data = {
            'status': 'success',
            'data': None,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)

    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.get('/get-categories')
async def get_categories_route(
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)

        # Получение категорий пользователя
        categories = await get_categories(session, user)

        response_data = {
            'status': 'success',
            'data': categories,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)
    
    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.post('/create-category')
async def create_category_route(
    category: CategoryCreate,
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)

        # Проверка на наличие такой категории у пользователя
        category_in_db = await get_category_by_title(session, category.title)
        if category_in_db:
            raise HTTPException(status_code=409, detail='Category already created')

        # Создание категории
        new_category = await create_category(session, user, category)

        response_data = {
            'status': 'success',
            'data': new_category,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)
    
    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.delete('/delete-category')
async def delete_category_route(
    category: CategoryDelete,
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)

        # Удаление счета пользователя
        await delete_category(session, user, category)

        response_data = {
            'status': 'success',
            'data': None,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)

    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.put('/edit-category')
async def edit_category_route(
    category: СategoryEdit,
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)

        # Проверка на наличие такой категории у пользователя
        # Ошибка только при разных id категорий
        category_in_db = await get_category_by_title(session, category.title)
        if category_in_db and category.id != category_in_db.category_id:
            raise HTTPException(status_code=409, detail='Category already created')

        # Изменение счета пользователя
        await edit_category(session, category)

        response_data = {
            'status': 'success',
            'data': None,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)
    
    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.get('/get-operations')
async def get_operations_route(
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)

        # Получение категорий пользователя
        operations = await get_operations(session, user)

        response_data = {
            'status': 'success',
            'data': operations,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)
    
    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.post('/create-operation')
async def create_operation_route(
    operation: OperationCreate,
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)

        # Создание операции
        new_operation = await create_operation(session, user, operation)

        response_data = {
            'status': 'success',
            'data': new_operation,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)
    
    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.delete('/delete-operation')
async def delete_operation_route(
    operation: OperationDelete,
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)

        # Удаление опрерации
        await delete_operation(session, operation)

        response_data = {
            'status': 'success',
            'data': None,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)
    
    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.put('/edit-operation')
async def edit_category_route(
    operation: OperationEdit,
    token = Depends(oauth2_scheme),
    session = Depends(get_async_session)
):
    try:
        # Получение данных о пользователе
        user = await get_current_user(token)

        # Изменение операции пользователя
        await edit_operation(session, operation)

        response_data = {
            'status': 'success',
            'data': None,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)
    
    except HTTPException as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': error.detail
        }
        return JSONResponse(content=response_data, status_code=error.status_code)

    except Exception as error:
        print(error)
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)