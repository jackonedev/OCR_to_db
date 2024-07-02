FROM python:3.10-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY ocr_service/requirements.txt .
RUN python -m pip install -r requirements.txt

RUN apt-get update && \
apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-spa

WORKDIR /app
COPY ./ocr_service /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
