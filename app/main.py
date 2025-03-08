from fastapi import FastAPI
from app.tasks.handlers import router as tasks_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_router


app = FastAPI()

routers = [tasks_router, auth_router, user_router]

for router in routers:
    app.include_router(router)
