from fastapi import FastAPI

from ocr_service.api import service

app = FastAPI()


app.include_router(service.router)


@app.get("/")
async def greetings():
    return {"message": "Hola mundo"}
