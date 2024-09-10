from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Float
from sqlalchemy.orm import relationship

from src.database import Base


class Operation(Base):
    '''
    Модель операций (доходов/расходов/переводов)
    '''

    __tablename__ = 'operation'

    operation_id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    operation_type = Column(String, nullable=False)
    from_account = Column(Integer, nullable=False)
    to_account = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    about = Column(String(length=1024))

    # Связь с таблицей User
    user = relationship('User', back_populates='operations')


class Account(Base):
    '''
    Модель счетов пользователей
    '''

    __tablename__ = 'account'

    account_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    balance = Column(Float, nullable=False)
    currency = Column(String, nullable=False)

    # Связь с таблицей User
    user = relationship('User', back_populates='accounts')


class Category(Base):
    '''
    Модель категорий расходов/доходов
    '''

    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    category_type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    color = Column(String)

    # Связь с таблицей User
    user = relationship('User', back_populates='categories')