from fastapi import FastAPI
from . import auth
from . import clothes
#SmartWardrobe

app = FastAPI()

@app.get("/")
def root():
    return {"mensagem": "API Guarda Roupa rodando"}

app.include_router(auth.router)
app.include_router(clothes.router)