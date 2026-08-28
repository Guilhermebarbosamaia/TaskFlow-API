# main.py
from database import Base, engine
from fastapi import FastAPI
from routers import auth, tasks, users

# Register all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

# Register Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)