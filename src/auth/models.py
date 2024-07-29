from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
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
    categories = relationship('Category', back_populates='user')