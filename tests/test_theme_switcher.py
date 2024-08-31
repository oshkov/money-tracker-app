import pytest

from config_test import client


# Тест регистрации
@pytest.mark.asyncio(scope='session')
async def test_news(client):
    # Отправка данных
    response = await client.post('/switch-theme')
    
    # Проверка успешного ответ
    assert response.status_code == 200