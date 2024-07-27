'''

Все модели используемые в проекте

'''


from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    '''
    Модель пользователей
    '''

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Связи с другими таблицами
    operations = relationship('Operation', back_populates='user')
    accounts = relationship('Account', back_populates='user')


class Operation(Base):
    '''
    Модель операций (доходов/расходов/переводов)
    '''

    __tablename__ = 'operation'

    operation_id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    operation_type = Column(String, nullable=False)
    from_account = Column(String, nullable=False)
    to_account = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    about = Column(String(length=1024), nullable=False)

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
    balance = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)

    # Связь с таблицей User
    user = relationship('User', back_populates='accounts')