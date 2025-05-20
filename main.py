from fastapi import FastAPI
from routes.store import router as store_router
from routes.users import router as users_router
from routes.auth import router as auth_router
from routes.admin import router as admin_router

app = FastAPI()

app.include_router(store_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/")
async def home():
    return {
        "message": "hello world..!"
    }