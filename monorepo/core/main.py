from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class BaseLedgerOperation(BaseModel): #serializer
    oki:int
    nama:int



@app.get('/')
def index():
    return {"message": "Hello World"}

@app.get('/greet/{name}')
def greet_name(name:str):
    return{"greeting":f"Hello{name}"}
@app.put('/item/{item_id}')
def up_item(item_id:int, )
