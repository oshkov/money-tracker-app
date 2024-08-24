# Трекер доходов и расходов на FastAPI

Этот сайт был создан с целью изучения FastAPI и других востребованных технологий.


### В проекте были использованы:

- FastApi
- PostgreSQL (SQLalchemy + asyncpg) 
- Pydantic
- Alembic
- Redis (aioredis)
- JavaScript (ajax)
- Pytest (async)
- Docker, Docker-compose

### Аутентификация

Аутентификация работает по схеме JWT+cookies. При регистрации или входе в аккаунт создается куки с jwt-токеном на 60 минут. Таким образом исключаются лишние запросы в бд для перехода пользователя между страницами.

### Структура базы данных

![image](https://github.com/user-attachments/assets/2a84d798-262a-4050-9472-08a8c9c7582a)

### Использование Redis

Redis используется на главной странице для кэширования списка новостей.

### Использование Ajax

Ajax используется во всех запросах пользователя

### Использование Docker-compose

Docker-compose включает в себя 3 контейнера: PostgreSQL, Redis и само приложение.


## Запуск

Запуск docker-compose:
```
docker-compose up --build -d
```

Запуск миграций (После запуска docker-compose):
```
docker-compose exec app alembic upgrade head
```
