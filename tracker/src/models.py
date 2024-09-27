from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float

from src.database import Base


class Operation(Base):
    '''
    Модель операций (доходов/расходов/переводов)
    '''

    __tablename__ = 'operation'

    operation_id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    user_id = Column(Integer, nullable=False)
    operation_type = Column(String, nullable=False)
    from_account = Column(Integer, nullable=False)
    to_account = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    about = Column(String(length=1024))


class Account(Base):
    '''
    Модель счетов пользователей
    '''

    __tablename__ = 'account'

    account_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    balance = Column(Float, nullable=False)
    currency = Column(String, nullable=False)


class Category(Base):
    '''
    Модель категорий расходов/доходов
    '''

    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    category_type = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    color = Column(String)