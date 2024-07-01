# OCR_to_db
La idea es pasar de una imagen a un registro en una tabla dentro de una base de datos SQL. El producto final involucra la gestion de la base de datos por medio de inteligencia artificial. También se pretende aceptar queries en natural language. El mayor esfuerzo se pondrá en la infraestructura de pipelines CI/CD- microservicios - web frameworks


## Instalando el modelo OCR en el container:

```devcontainer.json
"postCreateCommand": "sudo apt-get update && sudo apt-get install -y vim tesseract-ocr libtesseract-dev tesseract-ocr-spa",
```

**Para el modelo en español se debe instalar:**
`sudo apt-get install tesseract-ocr-spa`

Ref:
https://tesseract-ocr.github.io/tessdoc/Installation.html




## TODOs:
* pasar la imagen del devcontainer.json a un docker-compose.yml file para incorporar nuevos servicios (PostgreSQL)
