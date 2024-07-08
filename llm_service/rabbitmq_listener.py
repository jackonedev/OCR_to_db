import os
from api.middleware_in import RabbitMQReceiver


# Receiver from ocr_service/api/service.py: POST /ocr/images
receiver = RabbitMQReceiver(queue="ocr_llm")
# NOTE: consider sending a callable to the constructor of RabbitMQReceiver
receiver.start_consuming()
