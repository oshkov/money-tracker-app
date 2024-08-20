import pytest
from sqlalchemy import select

from src.tracker.models import Account, Category, Operation
from config_test import client, prepare_database, async_session_maker_test


# Тест регистрации для последующих тестов
@pytest.mark.asyncio(scope='session')
async def test_register(client):
    # Данные для регистрации
    data = {
        'username': 'string',
        'email': 'string',
        'password': 'string'
    }

    # Отправка данных
    response = await client.post('/register', json=data)

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест получения счетов пользователя
@pytest.mark.asyncio(scope='session')
async def test_get_accounts(client):
    # Отправка данных
    response = await client.get('/get-accounts')

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест получения категорий пользователя
@pytest.mark.asyncio(scope='session')
async def test_get_categories(client):
    # Отправка данных
    response = await client.get('/get-categories')

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест получения операций пользователя
@pytest.mark.asyncio(scope='session')
async def test_get_operations(client):
    # Отправка данных
    response = await client.get('/get-operations')

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест создания счета для пользователя
@pytest.mark.asyncio(scope='session')
async def test_create_account(client):
    data = {
        "title": "string",
        "balance": 0,
        "currency": "string"
    }

    # Отправка данных
    response = await client.post('/create-account', json=data)

    # Проверка на создание записи в бд
    async with async_session_maker_test() as session:
        account = await session.execute(select(Account).filter(Account.account_id == 1))
        account = account.scalars().first()

        assert account.title == data['title']

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест создания категории для пользователя
@pytest.mark.asyncio(scope='session')
async def test_create_category(client):
    data = {
        "title": "string",
        "category_type": "string",
        "color": "string"
    }

    # Отправка данных
    response = await client.post('/create-category', json=data)

    # Проверка на создание записи в бд
    async with async_session_maker_test() as session:
        category = await session.execute(select(Category).filter(Category.category_id == 1))
        category = category.scalars().first()

        assert category.title == data['title']

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест создания операции для пользователя
@pytest.mark.asyncio(scope='session')
async def test_create_operation(client):
    data = {
        "operation_type": "string",
        "from_account": 0,
        "to_account": 0,
        "amount": 0,
        "currency": "string",
        "about": "string"
    }

    # Отправка данных
    response = await client.post('/create-operation', json=data)

    # Проверка на создание записи в бд
    async with async_session_maker_test() as session:
        operation = await session.execute(select(Operation).filter(Operation.operation_id == 1))
        operation = operation.scalars().first()

        assert operation.about == data['about']

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест редактирования счета
@pytest.mark.asyncio(scope='session')
async def test_edit_account(client):
    data = {
        "id": 1,
        "title": "new_string",
        "balance": 0,
        "currency": "string"
    }

    # Отправка данных
    response = await client.put('/edit-account', json=data)

    # Проверка на изменение записи в бд
    async with async_session_maker_test() as session:
        account = await session.execute(select(Account).filter(Account.account_id == 1))
        account = account.scalars().first()

        assert account.title == data['title']

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест редактирования категории
@pytest.mark.asyncio(scope='session')
async def test_edit_category(client):
    data = {
        "id": 1,
        "title": "new_string",
        "color": "string"
    }

    # Отправка данных
    response = await client.put('/edit-category', json=data)

    # Проверка на создание записи в бд
    async with async_session_maker_test() as session:
        category = await session.execute(select(Category).filter(Category.category_id == 1))
        category = category.scalars().first()

        assert category.title == data['title']

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест редактирования операции
@pytest.mark.asyncio(scope='session')
async def test_edit_operation(client):
    data = {
        "id": 1,
        "from_account": 0,
        "to_account": 0,
        "amount": 0,
        "currency": "string",
        "about": "new_string"
    }

    # Отправка данных
    response = await client.put('/edit-operation', json=data)

    # Проверка на создание записи в бд
    async with async_session_maker_test() as session:
        operation = await session.execute(select(Operation).filter(Operation.operation_id == 1))
        operation = operation.scalars().first()

        assert operation.about == data['about']

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест удаления счета
@pytest.mark.asyncio(scope='session')
async def test_delete_account(client):
    data = {"id": 1}

    # Отправка данных
    response = await client.request(method='delete', url='/delete-account', json=data)

    # Проверка на удаление записи из бд
    async with async_session_maker_test() as session:
        account = await session.execute(select(Account).filter(Account.account_id == 1))
        account = account.scalars().first()

        assert account is None

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест удаления категории
@pytest.mark.asyncio(scope='session')
async def test_delete_category(client):
    data = {"id": 1}

    # Отправка данных
    response = await client.request(method='delete', url='/delete-category', json=data)

    # Проверка на создание записи в бд
    async with async_session_maker_test() as session:
        category = await session.execute(select(Category).filter(Category.category_id == 1))
        category = category.scalars().first()

        assert category is None

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест удаления операции
@pytest.mark.asyncio(scope='session')
async def test_operation_category(client):
    data = {"id": 1}

    # Отправка данных
    response = await client.request(method='delete', url='/delete-operation', json=data)

    # Проверка на создание записи в бд
    async with async_session_maker_test() as session:
        operation = await session.execute(select(Operation).filter(Operation.operation_id == 1))
        operation = operation.scalars().first()

        assert operation is None

    # Проверка успешного ответ
    assert response.status_code == 200