from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')


@router.get('/')
async def main_page(request: Request):
    # Получение темы из куки
    theme = request.cookies.get('theme')

    return templates.TemplateResponse('main.html', {'request': request, 'theme': theme})


@router.get('/register')
async def register_page(request: Request):
    # Получение темы из куки
    theme = request.cookies.get('theme')

    return templates.TemplateResponse('register.html', {'request': request, 'theme': theme})


@router.get('/login')
async def login_page(request: Request):
    # Получение куки
    cookies = request.cookies

    # Получение темы из куки
    theme = cookies.get('theme')

    return templates.TemplateResponse('login.html', {'request': request, 'theme': theme})


@router.get('/dashboard')
async def dashboard(request: Request):
    # Получение куки
    cookies = request.cookies

    # Получение темы из куки
    theme = cookies.get('theme')

    return templates.TemplateResponse('dashboard.html', {'request': request, 'theme': theme})


@router.get('/operations')
async def operations(request: Request):
    # Получение куки
    cookies = request.cookies

    # Получение темы из куки
    theme = cookies.get('theme')

    return templates.TemplateResponse('operations.html', {'request': request, 'theme': theme})


@router.get('/profile')
async def profile(request: Request):
    # Получение куки
    cookies = request.cookies

    # Получение темы из куки
    theme = cookies.get('theme')

    return templates.TemplateResponse('profile.html', {'request': request, 'theme': theme})