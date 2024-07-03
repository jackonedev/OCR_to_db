[![CI pipeline with Github Actions](https://github.com/jackonedev/OCR_to_db/actions/workflows/ci_pipeline.yml/badge.svg)](https://github.com/jackonedev/OCR_to_db/actions/workflows/ci_pipeline.yml)
# OCR_to_db
A partir de una fotogrofía de un ticket comercial, un modelo la transforma a texto, para luego ser procesada por otro modelo que extraerá la información para almacenarla en una base de datos relacional.

La arquitectura es por micro-servicios, actualmente se encuentran en desarrollo:
- ocr_service: con el modelo Tesseract para Optical Character Recognition, en su versión en Inglés y en Spanish.
- llm_service: (En desarrollo), modelos LLM de OpenAI integrado por medio de la interface de Langchain.
- RabbitMQ: (en desarrollo) el servicio que comunica ambos servicios.
- PostgreSQL: (on hang) para autocompletado de tablas por medio LLM, y gestión de usuario.


La idea es pasar de una imagen a un registro en una tabla dentro de una base de datos SQL. El producto final involucra la gestion de la base de datos por medio de inteligencia artificial. También se pretende aceptar queries en natural language. Los servicios se comunican por API REST utilizando FastAPI.


## Run the poject

1. Run `docker compose up` and the app would be running exposing port 8000.
2. Check if `localhost:8000` is running on the browser (you will see a hello message).
3. Go to `localhost:8000/docs` and click on "Try it out" in the OCR tag.
4. Use the interface to make a POST request to the `localhost:8000/ocr/images`, you can upload one or many images (that must contain text), and also set the language to Spanish or English.
5. Click on the "Execute" button and check the response.