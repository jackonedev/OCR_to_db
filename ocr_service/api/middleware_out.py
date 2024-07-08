import os
import time
import uuid
from contextlib import contextmanager

import pika

rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
rabbitmq_port = int(os.getenv("RABBITMQ_PORT", "5672"))


class RabbitMQClient:
    """
    A class representing a RabbitMQ client.

    Attributes:
        host (str): The RabbitMQ server host.
        request_queue (str): The name of the request queue.
        response_queue (str): The name of the response queue.
        corr_id (str): The correlation ID for the request.
        response (str): The response received from the server.

    Methods:
        on_response: Callback function for handling the server response.
        send_message: Sends a message to the server.
        get_response: Waits for and retrieves the server response.

    """

    def __init__(self, host=rabbitmq_host, request_queue="default"):
        self.host = host
        self.request_queue = request_queue
        self.response_queue = None
        self.corr_id = None
        self.response = None

    def on_response(self, ch, method, props, body):
        """
        Callback function for handling the server response.

        Args:
            ch: The channel object.
            method: The method object.
            props: The properties object.
            body: The response body.

        """
        if self.corr_id == props.correlation_id:
            self.response = body

    def send_message(self, channel, message):
        """
        Sends a message to the server.

        Args:
            channel: The channel object.
            message: The message to be sent.

        """
        self.corr_id = str(uuid.uuid4())
        channel.basic_publish(
            exchange="",
            routing_key=self.request_queue,
            properties=pika.BasicProperties(
                reply_to=self.response_queue, correlation_id=self.corr_id
            ),
            body=message,
        )

    def get_response(self, connection, timeout=10):
        """
        Waits for and retrieves the server response.

        Args:
            connection: The connection object.
            timeout (int): The maximum time to wait for a response (in seconds).

        Returns:
            str: The server response.

        Raises:
            TimeoutError: If no response is received within the timeout period.

        """
        start_time = time.time()
        while self.response is None:
            if time.time() - start_time > timeout:
                raise TimeoutError("No response received within the timeout period")
            connection.process_data_events()
        return self.response


@contextmanager
def rabbitmq_context(host=rabbitmq_host, request_queue="default"):
    """
    Creates a RabbitMQ context for handling requests and responses.

    Args:
        host (str, optional): The RabbitMQ host. Defaults to "localhost".
        request_queue (str, optional): The name of the request queue. Defaults to "default".

    Yields:
        tuple: A tuple containing the RabbitMQ client, connection, and channel.

    Raises:
        pika.exceptions.AMQPConnectionError: If a connection to RabbitMQ cannot be established.

    ```
    # Usage example:
    with rabbitmq_context(host='localhost', request_queue='my_queue') as (client, connection, channel):
        client.send_message(channel, 'Hello, RabbitMQ!')
        try:
            response = client.get_response(connection, timeout=30)
            print(f"Received response: {response}")
        except TimeoutError as e:
            print(str(e))
    ```

    """
    client = RabbitMQClient(host, request_queue)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=rabbitmq_port,
            virtual_host="/",
            credentials=pika.PlainCredentials("guest", "guest"),
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=request_queue)

    # Declare a unique callback queue for responses
    result = channel.queue_declare(queue="", exclusive=True)
    client.response_queue = result.method.queue

    # Set up basic consume on the callback queue
    channel.basic_consume(
        queue=client.response_queue,
        on_message_callback=client.on_response,
        auto_ack=True,
    )

    try:
        yield client, connection, channel
    finally:
        connection.close()
