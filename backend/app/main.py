from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . import auth
from . import clothes
from . import settings
#SmartWardrobe

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def root():
    return {"mensagem": "API Guarda Roupa rodando"}

app.include_router(auth.router)
app.include_router(clothes.router)
app.include_router(settings.router)