from sqlalchemy import select, or_
from datetime import datetime, timedelta

from src.tracker.models import Account, Category, Operation
from src.auth.schemas import UserRead
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


# Проверка наличия такого счета у пользователя
async def get_account_by_title(session, title):

    try:
        # Проверка на наличие пользователя в таблице
        result = await session.execute(select(Account).filter(Account.title == title))
        account = result.scalars().first()
        return account

    except Exception as error:
        raise error


# Создание счета
async def create_account(session, user: UserRead, account: AccountCreate):

    try:
        account_info = Account(
            title = account.title,
            user_id = user.id,
            balance = account.balance,
            currency = account.currency
        )

        # Добавление данных в сессию
        session.add(account_info)

        # Добавление данных в бд и сохранение
        await session.commit()

        return {
            'account_id': account_info.account_id,
            'title': account_info.title,
            'balance': account_info.balance,
            'currency': account_info.currency
        }

    except Exception as error:
        raise error
    

# Удаление счета
async def delete_account(session, account: AccountDelete):

    try:
        account_info = await session.get(Account, account.id)

        # Получение всех операций связанных с этим счетом
        operations = await session.execute(
            select(Operation)
                .where(
                    or_(
                        Operation.from_account == account_info.account_id,
                        Operation.to_account == account_info.account_id
                    )
                )
            )
        operations = operations.scalars().all()

        # Удаление операций
        for operation in operations:
            await session.delete(operation)

        # Удаление счета
        await session.delete(account_info)

        # Добавление данных в бд и сохранение
        await session.commit()

    except Exception as error:
        raise error
    

# Изменение счета
async def edit_account(session, account: AccountEdit):

    try:
        account_info = await session.get(Account, account.id)

        account_info.title = account.title
        account_info.balance = account.balance
        account_info.currency = account.currency

        # Добавление данных в бд и сохранение
        await session.commit()

    except Exception as error:
        raise error
    

# Проверка наличия такой категории у пользователя
async def get_category_by_title(session, title):

    try:
        # Проверка на наличие пользователя в таблице
        result = await session.execute(select(Category).filter(Category.title == title))
        category = result.scalars().first()
        return category

    except Exception as error:
        raise error
    

# Создание категории
async def create_category(session, user: UserRead, category: CategoryCreate):

    try:
        category_info = Category(
            title = category.title,
            category_type = category.category_type,
            user_id = user.id,
            color = category.color
        )

        # Добавление данных в сессию
        session.add(category_info)

        # Добавление данных в бд и сохранение
        await session.commit()

        return {
            'category_id': category_info.category_id,
            'title': category_info.title,
            'category_type': category_info.category_type,
            'color': category_info.color
        }

    except Exception as error:
        raise error
    

# Удаление категории
async def delete_category(session, user, category: CategoryDelete):

    try:
        category_info = await session.get(Category, category.id)

        # Получение всех операций связанных с этой категорией
        operations = await session.execute(
            select(Operation)
                .where(
                    or_(
                        Operation.from_account == category_info.category_id,
                        Operation.to_account == category_info.category_id
                    )
                )
            )
        operations = operations.scalars().all()

        # Удаление операций
        for operation in operations:
            await session.delete(operation)

        # Удаление категории
        await session.delete(category_info)

        # Добавление данных в бд и сохранение
        await session.commit()

    except Exception as error:
        raise error


# Изменение счета
async def edit_category(session, category: СategoryEdit):

    try:
        account_info = await session.get(Category, category.id)

        account_info.title = category.title
        account_info.color = category.color

        # Добавление данных в бд и сохранение
        await session.commit()

    except Exception as error:
        raise error


# Создание операции
async def create_operation(session, user: UserRead, operation: OperationCreate):

    try:
        # В случае пополнения баланса
        if operation.operation_type == 'income':
            account_to = await session.get(Account, operation.to_account)
            account_to.balance = account_to.balance + operation.amount

        # В случае расхода
        elif operation.operation_type == 'expense':
            # Вычет баланса со счета
            account_from = await session.get(Account, operation.from_account)
            account_from.balance = account_from.balance - operation.amount

        # В случае перевода пополнение баланса на втором счету
        elif operation.operation_type == 'transfer':
            account_to = await session.get(Account, operation.to_account)

            # Ошибка перевода в случае разных валют счетов
            if account_from.currency != account_to.currency:
                raise RuntimeError

            # Пополнение баланса второго счета
            account_to.balance = account_to.balance + operation.amount

        operation_info = Operation(
            user_id = user.id,
            operation_type = operation.operation_type,
            from_account = operation.from_account,
            to_account = operation.to_account,
            amount = operation.amount,
            currency = operation.currency,
            about = operation.about
        )

        # Добавление данных в сессию
        session.add(operation_info)

        # Добавление данных в бд и сохранение
        await session.commit()

        return {
            'operation_id': operation_info.operation_id,
            'created_at': operation_info.created_at.strftime('%d.%m.%y'),
            'operation_type': operation_info.operation_type,
            'from_account': operation_info.from_account,
            'to_account': operation_info.to_account,
            'amount': operation_info.amount,
            'currency': operation_info.currency,
            'about': operation_info.about
        }

    except Exception as error:
        raise error
    

# Удаление операции
async def delete_operation(session, operation: OperationDelete):

    try:
        operation_info = await session.get(Operation, operation.id)

        await session.delete(operation_info)

        # Добавление данных в бд и сохранение
        await session.commit()

    except Exception as error:
        raise error


# Изменение операции
async def edit_operation(session, operation: OperationEdit):

    try:
        operation_info = await session.get(Operation, operation.id)

        operation_info.from_account = operation.from_account
        operation_info.to_account = operation.to_account
        operation_info.amount = operation.amount
        operation_info.currency = operation.currency
        operation_info.about = operation.about

        # Добавление данных в бд и сохранение
        await session.commit()

    except Exception as error:
        raise error
    

# Получение всех счетов пользователя
async def get_accounts(session, user):
    try:
        result = await session.execute(select(Account).filter(Account.user_id == user.id))
        accounts = result.scalars()
        accounts_array = []
        for account in accounts:
            account_dict = {
                'account_id': account.account_id,
                'title': account.title,
                'balance': account.balance,
                'currency': account.currency
            }
            accounts_array.append(account_dict)

        return accounts_array

    except Exception as error:
        raise error
    

# Получение всех категорий пользователя
async def get_categories(session, user):
    try:
        result = await session.execute(select(Category).filter(Category.user_id == user.id))
        categories = result.scalars()
        categories_array = []
        for category in categories:
            category_dict = {
                'category_id': category.category_id,
                'title': category.title,
                'category_type': category.category_type,
                'color': category.color
            }
            categories_array.append(category_dict)

        return categories_array

    except Exception as error:
        raise error
    

# Получение всех операций пользователя за месяц
async def get_operations(session, user):
    try:
        # Определяем начало и конец текущего месяца
        now = datetime.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

        result = await session.execute(
            select(Operation).filter(
                Operation.user_id == user.id,
                Operation.created_at >= start_of_month,
                Operation.created_at <= end_of_month
            )
        )
        operations = result.scalars()

        operations_array = []
        for operation in operations:
            operation_dict = {
                'operation_id': operation.operation_id,
                'created_at': operation.created_at.strftime('%d.%m.%y'),
                'operation_type': operation.operation_type,
                'from_account': operation.from_account,
                'to_account': operation.to_account,
                'amount': operation.amount,
                'currency': operation.currency,
                'about': operation.about,
            }
            operations_array.append(operation_dict)

        return operations_array

    except Exception as error:
        raise error
