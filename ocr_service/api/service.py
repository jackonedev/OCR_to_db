"""
Aquí se encuentra la lógica de la API de OCR, que se encarga de recibir las
imagenes, procesarlas y enviar el texto obtenido al servicio de LLM, y 
esperar la respuesta de este último.
"""

import asyncio
import os
import socket
import tempfile
from typing import Annotated

import pika
from fastapi import APIRouter, File, HTTPException, UploadFile

from ocrlogic.ocr_core import ocr_core
from utils.schemas import OCRLanguage

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
    lang: OCRLanguage = "eng",
):
    """
    Recibe una imagen y la procesa para obtener el texto que contiene.

    Ademas, envía el texto al servicio de LLM por medio de RabbitMQ queue.
    Si el servicio está disponible espera la inferencia y la incluye en la respuesta.
    El LLM retorna un esquema tipo tabla de los datos encontrados en el texto.
    Los esquemas de tabla solo incluyen Ticket de compras.
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
    except socket.gaierror:
        print("Error: Name or service not known. Could not stablish the connection.")
    # pylint: disable=W0718
    except Exception as e:
        print(f"Unexpected Error: {e}")

    # Delete temporary files
    for temp_file in temp_file_paths:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    # Save params
    response["ocr_lang"] = lang

    return response
