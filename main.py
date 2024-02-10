import uvicorn
from fastapi import FastAPI, APIRouter
from src.api.handlers import user_router

app = FastAPI(title="pet-shop")


main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
