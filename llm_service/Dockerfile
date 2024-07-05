FROM python:3.10-slim

EXPOSE 8001

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY llm_service/requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY ./ocr_service /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["langchain", "app", "serve", "--app", "main:app", "--host", "0.0.0.0", "--port", "8001"]