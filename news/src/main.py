from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.router import router as news_router


app = FastAPI(title='news_service')


app.include_router(news_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000", f"http://185.237.165.219:8000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)