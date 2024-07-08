"""
Aquí se encuentra la lógica de la API de OCR, que se encarga de recibir las
imagenes, procesarlas y enviar el texto obtenido al servicio de LLM, y 
esperar la respuesta de este último.
"""

import asyncio
import os
import tempfile
from typing import Annotated

import pika
from fastapi import APIRouter, File, HTTPException, UploadFile

from ocrlogic.ocr_core import ocr_core

from .middleware_out import rabbitmq_context

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
    temp_file_paths = []
    for img in images:
        print("Images Uploaded: ", img.filename)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_paths.append(temp_file.name)
            await img.seek(0)
            with open(temp_file_paths[-1], "wb") as temp_file:
                temp_file.write(await img.read())
            tasks.append(
                asyncio.create_task(ocr_core(img_path=temp_file_paths[-1], lang=lang))
            )

    # OCR execution
    try:
        texts = await asyncio.gather(*tasks)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    for i, text in enumerate(texts):
        response[images[i].filename] = [text]

    # Send text to LLM service
    try:
        with rabbitmq_context(request_queue="ocr_llm") as (
            client,
            connection,
            channel,
        ):
            for i, k in enumerate(list(response.keys())):
                client.send_message(channel, response[k][0])
                try:
                    llm_response = client.get_response(connection, timeout=8)
                    print(f"Received response: {llm_response}")
                    response[images[i].filename].append(llm_response)
                except TimeoutError as e:
                    print(str(e))
                    response[images[i].filename].append(
                        "No response received within the timeout period"
                    )
    except pika.exceptions.AMQPConnectionError as e:
        print(str(e))
        raise HTTPException(
            status_code=503, detail="RabbitMQ Service Unavailable"
        ) from e

    # Delete temporary files
    for temp_file in temp_file_paths:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return response
