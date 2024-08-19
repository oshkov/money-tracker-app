import pytest
from sqlalchemy import select

from config_test import client, prepare_database


# Тест регистрации
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


# Тест логина
@pytest.mark.asyncio(scope='session')
async def test_login(client):
    # Данные для входа
    data = {
        'email': 'string',
        'password': 'string'
    }

    # Отправка данных
    response = await client.post('/login', json=data)

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест редактирования профиля
@pytest.mark.asyncio(scope='session')
async def test_edit_profile(client):
    # Данные для изменения аккаунта
    data = {
        "username": "string",
        "email": "string",
        "password": "string"
    }

    # Отправка данных
    response = await client.post('/edit-profile', json=data)

    # Проверка успешного ответ
    assert response.status_code == 200


# Тест выхода из аккаунта
@pytest.mark.asyncio(scope='session')
async def test_logout(client):
    # Отправка данных
    response = await client.post('/logout')

    # Проверка успешного ответ
    assert response.status_code == 200