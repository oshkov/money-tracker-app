from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from src.auth.base_config import auth_backend, fastapi_users, current_user
from src.auth.schemas import UserCreate, UserRead
from src.auth.models import User


app = FastAPI(title='MoneyTrackerApp')
app.mount('/src/static', StaticFiles(directory='src/static'), name='static')

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)



@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"
