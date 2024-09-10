from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth.router import router as auth_router
from src.pages.router import router as page_router
from src.tracker.router import router as tracker_router


app = FastAPI(title='MoneyTrackerApp')
app.mount('/src/static', StaticFiles(directory='src/static'), name='static')


app.include_router(auth_router)
app.include_router(page_router)
app.include_router(tracker_router)