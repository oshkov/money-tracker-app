from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.database import get_async_session
from src.auth.schemas import UserRead
from src.auth.utils import get_current_user
from src.tracker.schemas import (
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
from src.tracker.utils import (
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

@router.get('/get-accounts')
async def get_accounts_route(
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Получение счетов пользователя
        accounts = await get_accounts(session, user)

        response_data = {
            'status': 'success',
            'data': accounts,
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


@router.post('/create-account')
async def create_account_route(
    account: AccountCreate,
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Проверка на наличие такого счета у пользователя
        account_in_db = await get_account_by_title(session, account.title)
        if account_in_db:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Account already created'
            }
            return JSONResponse(content=response_data, status_code=409)

        # Создание счета пользователя
        await create_account(session, user, account)

        response_data = {
            'status': 'success',
            'data': None,
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


@router.delete('/delete-account')
async def delete_account_route(
    account: AccountDelete,
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Удаление счета пользователя
        await delete_account(session, account)

        response_data = {
            'status': 'success',
            'data': None,
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


@router.put('/edit-account')
async def edit_account_route(
    account: AccountEdit,
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Проверка на наличие такого счета у пользователя
        # Ошибка только при разных id счетов
        account_in_db = await get_account_by_title(session, account.title)
        if account_in_db and account.id != account_in_db.account_id:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Account already created'
            }
            return JSONResponse(content=response_data, status_code=409)

        # Изменение счета пользователя
        await edit_account(session, account)

        response_data = {
            'status': 'success',
            'data': None,
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


@router.get('/get-categories')
async def get_categories_route(
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Получение категорий пользователя
        categories = await get_categories(session, user)

        response_data = {
            'status': 'success',
            'data': categories,
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


@router.post('/create-category')
async def create_category_route(
    category: CategoryCreate,
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Проверка на наличие такой категории у пользователя
        category_in_db = await get_category_by_title(session, category.title)
        if category_in_db:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Category already created'
            }
            return JSONResponse(content=response_data, status_code=409)

        # Создание категории
        await create_category(session, user, category)

        response_data = {
            'status': 'success',
            'data': None,
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


@router.delete('/delete-category')
async def delete_category_route(
    category: CategoryDelete,
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Удаление счета пользователя
        await delete_category(session, user, category)

        response_data = {
            'status': 'success',
            'data': None,
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


@router.put('/edit-category')
async def edit_category_route(
    category: СategoryEdit,
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Проверка на наличие такой категории у пользователя
        # Ошибка только при разных id категорий
        category_in_db = await get_category_by_title(session, category.title)
        if category_in_db and category.id != category_in_db.category_id:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Category already created'
            }
            return JSONResponse(content=response_data, status_code=409)

        # Изменение счета пользователя
        await edit_category(session, category)

        response_data = {
            'status': 'success',
            'data': None,
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


@router.get('/get-operations')
async def get_operations_route(
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Получение категорий пользователя
        operations = await get_operations(session, user)

        response_data = {
            'status': 'success',
            'data': operations,
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


@router.post('/create-operation')
async def create_operation_route(
    operation: OperationCreate,
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Создание операции
        await create_operation(session, user, operation)

        response_data = {
            'status': 'success',
            'data': None,
            'detail': None
        }
        return JSONResponse(content=response_data, status_code=200)
    
    except RuntimeError as error:
        response_data = {
            'status': 'error',
            'data': None,
            'detail': "You can't transfer money to account with another currency"
        }
        return JSONResponse(content=response_data, status_code=400)

    except Exception as error:
        response_data = {
            'status': 'error',
            'data': str(error),
            'detail': 'Server error'
        }
        return JSONResponse(content=response_data, status_code=500)


@router.delete('/delete-operation')
async def delete_operation_route(
    operation: OperationDelete,
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Удаление опрерации
        await delete_operation(session, operation)

        response_data = {
            'status': 'success',
            'data': None,
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


@router.put('/edit-operation')
async def edit_category_route(
    operation: OperationEdit,
    user: UserRead = Depends(get_current_user),
    session = Depends(get_async_session)
):
    try:
        # Проверка на авторизацию
        if user is None:
            response_data = {
                'status': 'error',
                'data': None,
                'detail': 'Not authenticated'
            }
            return JSONResponse(content=response_data, status_code=401)

        # Изменение операции пользователя
        await edit_operation(session, operation)

        response_data = {
            'status': 'success',
            'data': None,
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