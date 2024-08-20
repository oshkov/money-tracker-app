import pytest

from config_test import client, prepare_database


# Тест регистрации
@pytest.mark.asyncio(scope='session')
async def test_news(client):
    # Отправка данных
    response = await client.get('/get-news')
    
    # Проверка успешного ответ
    assert response.status_code == 200