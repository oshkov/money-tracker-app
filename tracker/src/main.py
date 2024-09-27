from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.router import router as tracker_router


app = FastAPI(title='tracker_service')


app.include_router(tracker_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000", "http://185.237.165.219:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["*"],
)