"""
Set the connection parameters to connect to localhost on port 5672
on the / virtual host using the username "dev" and password "dev123"
"""

import pika

credentials = pika.PlainCredentials(username="dev", password="dev123")

parameters = pika.ConnectionParameters(
    host="localhost", port=5672, virtual_host="/", credentials=credentials
)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()
