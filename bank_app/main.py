from fastapi import FastAPI
from bank_app.controllers.controller import router

app = FastAPI()

app.include_router(router, prefix="/bank", tags=["Bank Operations"])
