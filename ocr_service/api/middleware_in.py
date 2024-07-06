import pika


class RabbitMQReceiver:
    """
    -------------------------------------
    THIS CLASS IS A TEMPLATE
    THE self.process_message METHOD NEEDS
    TO BE IMPLEMENTED OR REMOVED
    -------------------------------------

    A class that receives messages from RabbitMQ and processes them.

    Args:
        host (str): The hostname or IP address of the RabbitMQ server. Default is "localhost".
        queue (str): The name of the queue to consume messages from. Default is "default".
    """

    def __init__(self, host="localhost", queue="default"):
        self.host = host
        self.queue = queue

    def on_message(self, ch, method, properties, body):
        """
        Callback function that is called when a message is received.

        Args:
            ch: The channel object.
            method: The method object.
            properties: The properties object.
            body: The message body.

        Returns:
            None
        """
        print(f"Received message: {body}")
        # Processing the message
        response = self.process_message(body)
        # sending the response
        self.send_response(response, properties.reply_to, properties.correlation_id)

    def process_message(self, body):
        """
        Process the received message.

        Args:
            body: The message body.

        Returns:
            str: The processed message.
        """
        # Some logic
        return f"Processed: {body}"

    def send_response(self, response, reply_to, correlation_id):
        """
        Send the response message.

        Args:
            response (str): The response message.
            reply_to (str): The reply-to queue name.
            correlation_id (str): The correlation ID.

        Returns:
            None
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        channel.basic_publish(
            exchange="",
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=response,
        )
        connection.close()

    def start_consuming(self):
        """
        Start consuming messages from the queue.

        Returns:
            None
        """
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
            print("Stopping receiver...")
            channel.stop_consuming()
        finally:
            connection.close()


# if __name__ == "__main__":
#     receiver = RabbitMQReceiver(host="localhost", queue="my_test_queue")
#     receiver.start_consuming()
