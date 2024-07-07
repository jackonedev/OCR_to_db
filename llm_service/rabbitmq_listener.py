from api.middleware_in import RabbitMQReceiver

# Receiver from ocr_service/api/service.py: POST /ocr/images
receiver = RabbitMQReceiver(host="localhost", queue="ocr_llm")
receiver.start_consuming()

# TODO: consider sending a callable to the constructor of RabbitMQReceiver
