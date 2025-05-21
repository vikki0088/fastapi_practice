from fastapi import FastAPI,Request
from routes.store import router as store_router
from routes.users import router as users_router
from routes.auth import router as auth_router
from routes.admin import router as admin_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount("/static",StaticFiles(directory="static"),name="static")

app.include_router(store_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(admin_router)



@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html",{'request': request})

