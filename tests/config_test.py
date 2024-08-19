import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.database import get_async_session, Base
from src.config import DATABASE_URL_TEST


test_engine = create_async_engine(DATABASE_URL_TEST)
async_session_maker_test = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


# Переопределение зависимости для тестов
async def override_get_async_session():
    async with async_session_maker_test() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

# Фикстура для тестовой базы данных
@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield 

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Асинхронный клиент
@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client