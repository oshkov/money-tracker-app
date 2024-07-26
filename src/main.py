from fastapi import FastAPI, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from src.auth.router import router as auth_router
from src.pages.router import router as page_router


app = FastAPI(title='MoneyTrackerApp')
app.mount('/src/static', StaticFiles(directory='src/static'), name='static')


app.include_router(auth_router)
app.include_router(page_router)