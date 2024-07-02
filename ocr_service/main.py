from fastapi import FastAPI

from api import service

app = FastAPI()


app.include_router(service.router)


@app.get("/")
async def greetings():
    return {"message": "Hola mundo"}
