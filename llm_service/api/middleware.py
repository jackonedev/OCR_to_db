#!/usr/bin/env python
"""
Set the connection parameters to connect to localhost on port 5672
on the / virtual host using the username "dev" and password "dev123"
"""

import os
import sys

import pika


def main():

    credentials = pika.PlainCredentials(username="dev", password="dev123")

    parameters = pika.ConnectionParameters(
        host="localhost", port=5672, virtual_host="/", credentials=credentials
    )

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue="ocr_llm_queue")

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(
        queue="ocr_llm_queue", on_message_callback=callback, auto_ack=True
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
