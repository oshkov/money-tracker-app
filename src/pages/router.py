from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.auth.schemas import UserRead
from src.auth.utils import get_current_user


router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router.get("/dashboard")
def dashboard(request: Request, user: UserRead = Depends(get_current_user)):
    # Проверка пользователя
    if user is None:
        return RedirectResponse(url='/login')

    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


@router.get("/operations")
def dashboard(request: Request, user: UserRead = Depends(get_current_user)):
    # Проверка пользователя
    if user is None:
        return RedirectResponse(url='/login')

    return templates.TemplateResponse("operations.html", {"request": request, "user": user})