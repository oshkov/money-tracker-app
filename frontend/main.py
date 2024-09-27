from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from router import router as page_router


app = FastAPI(title='frontend')
app.mount('/static', StaticFiles(directory='static'), name='static')


app.include_router(page_router)