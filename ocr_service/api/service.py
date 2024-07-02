"""
Aquí se encuentra la lógica de la API de OCR, que se encarga de recibir las
imagenes, procesarlas y enviar el texto obtenido al servicio de LLM, y 
esperar la respuesta de este último.
"""

import asyncio
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from .tools import _save_file_to_server
from ocrlogic.ocr_core import ocr_core
# from .middleware import send_job_to_llm

router = APIRouter(
    prefix="/ocr",
    tags=["OCR"],
)


@router.post("/images")
async def ocr_image(
    images: Annotated[
        list[UploadFile], File(description="Multiple Images with text to be extracted")
    ],
    lang: str = "eng",
):
    """
    Recibe una imagen y la procesa para obtener el texto que contiene.
    Luego envía el texto al servicio de LLM y retorna la respuesta de este.
    """

    response = {}
    tasks = []

    for img in images:
        print("Images Uploaded: ", img.filename)
        temp_file = _save_file_to_server(
            img, path="./", save_as=img.filename
        )
        tasks.append(asyncio.create_task(ocr_core(img_path=temp_file, lang=lang)))
    # Procesamos el texto y actualizamos la response
    texts = await asyncio.gather(*tasks)
    for i, text in enumerate(texts):
        response[images[i].filename] = [text]

    # Enviamos el texto al servicio de LLM
    # response = await send_job_to_llm(response)
    return response
