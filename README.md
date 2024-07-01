# OCR_to_db
[![CI pipeline with Github Actions](https://github.com/jackonedev/OCR_to_db/actions/workflows/ci_pipeline.yml/badge.svg)](https://github.com/jackonedev/OCR_to_db/actions/workflows/ci_pipeline.yml)

La idea es pasar de una imagen a un registro en una tabla dentro de una base de datos SQL. El producto final involucra la gestion de la base de datos por medio de inteligencia artificial. También se pretende aceptar queries en natural language. El mayor esfuerzo se pondrá en la infraestructura de pipelines CI/CD- monolithic service - web frameworks


## Instalando el modelo OCR en el container:

```devcontainer.json
"postCreateCommand": "sudo apt-get update && sudo apt-get install -y vim tesseract-ocr libtesseract-dev tesseract-ocr-spa",
```

**Para el modelo en español se debe instalar:**
`sudo apt-get install tesseract-ocr-spa`

Ref:
https://tesseract-ocr.github.io/tessdoc/Installation.html



## Instalacion del virtual environment

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
* Crear la notebook en colab para compartir
* crear la API para servicio
* pasar la imagen del devcontainer.json a un docker-compose.yml file para incorporar nuevos servicios (PostgreSQL)
