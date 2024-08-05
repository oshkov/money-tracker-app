from pydantic import BaseModel
from typing import Optional


class AccountCreate(BaseModel):
    title: str
    balance: float
    currency: str


class AccountDelete(BaseModel):
    id: int


class AccountEdit(AccountCreate, AccountDelete):
    pass


class CategoryCreate(BaseModel):
    title: str
    category_type: str
    color: Optional[str] = None


class CategoryDelete(BaseModel):
    id: int


class СategoryEdit(CategoryDelete):
    title: str
    color: Optional[str] = None


class OperationCreate(BaseModel):
    operation_type: str
    from_account: int
    to_account: int
    amount: float
    currency: str
    about: Optional[str] = None


class OperationDelete(BaseModel):
    id: int


class OperationEdit(OperationDelete):
    from_account: int
    to_account: int
    amount: float
    currency: str
    about: Optional[str] = None