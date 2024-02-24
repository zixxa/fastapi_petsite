import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI

from src.api.handlers import user_router
from src.api.login_handler import login_router

app = FastAPI(title="pet-shop")


main_api_router = APIRouter()

main_api_router.include_router(login_router, prefix="/login", tags=["login"])
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
