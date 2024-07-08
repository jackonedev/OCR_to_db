#!/usr/bin/env python
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from llmlogic.llm_core import chain as schematization_chain

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


schematization_chain = NotImplemented
add_routes(app, schematization_chain)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
