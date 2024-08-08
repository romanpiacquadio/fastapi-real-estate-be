import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core import auth
from app.core import users
from app.routes import views
from app.core.database import engine
from app.core.database import Base

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(views.router)
app.include_router(users.router, prefix="/api")

Base.metadata.create_all(bind=engine)