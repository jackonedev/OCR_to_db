#!/usr/bin/env python3
import pika

from llmlogic.llm_core import chain


class RabbitMQReceiver:
    def __init__(self, host="localhost", queue="default"):
        self.host = host
        self.queue = queue

    def on_message(self, ch, method, properties, body):
        "Callback function for retrieving answers from the message queue."
        print(f"Received message: {body}")
        # Processing the message
        response = self.process_message(body)
        # sending the response
        self.send_response(response, properties.reply_to, properties.correlation_id)

    def process_message(self, body):
        # TODO: consider sending a callable to the constructor of RabbitMQReceiver
        """
        Process the given message body using the langchain llmlogic/llm_core.py chain.
        """
        return chain.invoke(body)

    def send_response(self, response, reply_to, correlation_id):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
            channel = connection.channel()
            channel.basic_publish(
                exchange="",
                routing_key=reply_to,
                properties=pika.BasicProperties(correlation_id=correlation_id),
                body=response,
            )
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Attempt to connect failed: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            if "connection" in locals() and connection.is_open:
                connection.close()

    def start_consuming(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue)
        channel.basic_consume(
            queue=self.queue, on_message_callback=self.on_message, auto_ack=True
        )
        print(f"Waiting for messages in {self.queue}. To exit press CTRL+C")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print("\nStopping receiver...")
            channel.stop_consuming()
        finally:
            connection.close()
            print("Receiver stopped\n")
