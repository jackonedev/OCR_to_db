[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jackonedev/OCR_Testdrive/blob/main/OCR_Testdrive.ipynb)

[![CI pipeline with Github Actions](https://github.com/jackonedev/OCR_to_db/actions/workflows/ci_pipeline.yml/badge.svg)](https://github.com/jackonedev/OCR_to_db/actions/workflows/ci_pipeline.yml)
# OCR_to_db

## OCR Service

La finalidad de este componente es transformar imagenes en texto.
Se compone del modelo Google Tesseract en sus versiones en Inglés y Español, ejecutados de forma local y gestionados por medio de la librería `pytesseract`.
La lógica del modelo se encuentra encapsulada dentro de `ocrlogic/ocr_core/ocr_core.py` en donde cada input es primero buscado dentro de los archivos temporales de la api service, y si no lo encuentra lo busca dentro del directorio `static/img/`.

El componente cuenta con un servicio API cuyo unico endpoint es `{host}:{port}/ocr/images/` que acepta método POST. El endpoint posee el parametro `images` y `lang`, uno recibe un o multiples archivos y  el otro un texto que representa el lenguaje correspondiente al modelo que se debe ejecutar. A su vez, el endpoint posee una conexión con el micro-servicio **RabbitMQ**, por lo que cada request poseera la interpretación del texto obtenido por parte de un LLM que se aloja en otro micro-servicio llamado **LLM Service**.

En resumen, la lógica del modelo se encuentra en `ocrlogic/ocr_core.py`, la api se encuentra en `api/service.py`, la interfaz para las conexiones con RabbitMQ se encuentran en ~~`api/middleware_in.py`~~ y `api/middleware_out.py` que se encarga de generar las conexiones de forma segura.

### OCR Service Key Notes:
Para probar el servicio, cree un entorno de trabajo que puede ser un entorno virtual python, utilizando el comando `python -m venv .venv`, luego activar dicho entorno.

**Instalación del modelo: (caso Español)**
`sudo apt-get install tesseract-ocr-spa`

Ref:
https://tesseract-ocr.github.io/tessdoc/Installation.html



**Instalación de las dependencias:**

El resto de las dependencias pueden hacerse una vez activado el entorno adecuado con el comando `make install`

## Ejecucion por linea de comando

Puede simplificar la ejecucion por medio de `chmod -x ocr_cli.py`.
Luego puede ejecutar el fichero directamente desde un shell:

```shell
./ocr_cli.py --help
./ocr_cli.py --img_path="gran_registro"
./ocr_cli.py --img_path="gran_registro" --lang="spa"
```


## TODOs:
* ~~Crear la notebook en colab para compartir~~
* ~~crear la API para servicio y tests~~
* ~~agregar docker-compose.yml file para incorporar nuevos servicios (PostgreSQL, RabbitMQ)~~
* ~~generar middleware con RabbitMQ para conexion con llm_service~~
* ~~check for test that generates unnecessary files~~
* ~~aloud "eng+spa" option for lang parameter~~
* ~~create schema for the available language options~~
* Evaluate how image editing affects the OCR model performance