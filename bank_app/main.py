from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sys
import os
from bank_app.controllers import controller

app = FastAPI()

app.include_router(controller.router, prefix="/bank", tags=["Bank Operations"])
