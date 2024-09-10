from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.auth.schemas import UserRead
from src.auth.utils import get_current_user


router = APIRouter(
    tags=['Pages']
)

templates = Jinja2Templates(directory='src/templates')


@router.get('/')
def main_page(request: Request):
    # Получение темы из куки
    theme = request.cookies.get('theme')

    return templates.TemplateResponse('main.html', {'request': request, 'theme': theme})


@router.get('/register')
def register_page(request: Request):
    # Получение темы из куки
    theme = request.cookies.get('theme')

    return templates.TemplateResponse('register.html', {'request': request, 'theme': theme})


@router.get('/login')
def login_page(request: Request, user: UserRead = Depends(get_current_user)):
    # Получение темы из куки
    theme = request.cookies.get('theme')

    # Проверка пользователя
    if user:
        return RedirectResponse(url='/dashboard')

    return templates.TemplateResponse('login.html', {'request': request, 'theme': theme})


@router.get('/dashboard')
def dashboard(request: Request, user: UserRead = Depends(get_current_user)):
    # Получение темы из куки
    theme = request.cookies.get('theme')

    # Проверка пользователя
    if user is None:
        return RedirectResponse(url='/login')

    return templates.TemplateResponse('dashboard.html', {'request': request, 'user': user, 'theme': theme})


@router.get('/operations')
def operations(request: Request, user: UserRead = Depends(get_current_user)):
    # Получение темы из куки
    theme = request.cookies.get('theme')

    # Проверка пользователя
    if user is None:
        return RedirectResponse(url='/login')

    return templates.TemplateResponse('operations.html', {'request': request, 'user': user, 'theme': theme})


@router.get('/profile')
def profile(request: Request, user: UserRead = Depends(get_current_user)):
    # Получение темы из куки
    theme = request.cookies.get('theme')

    # Проверка пользователя
    if user is None:
        return RedirectResponse(url='/login')

    return templates.TemplateResponse('profile.html', {'request': request, 'user': user, 'theme': theme})