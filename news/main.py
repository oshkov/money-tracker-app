from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import router as news_router


app = FastAPI(title='MoneyTrackerApp')


app.include_router(news_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)