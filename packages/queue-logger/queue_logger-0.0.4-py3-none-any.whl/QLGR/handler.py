import os
import pika
import logging


class RabbitMQHandler(logging.Handler):
    def __init__(self, exchange='', level=logging.NOTSET):
        super().__init__(level)

        host = os.getenv("QUEUE_HOST")
        port = os.getenv("QUEUE_PORT")
        creds = pika.PlainCredentials(
            username=os.getenv("QUEUE_USER"),
            password=os.getenv("QUEUE_PASS")
        )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(credentials=creds, host=host, port=port)
        )
        channel = connection.channel()
        channel.queue_declare(queue='logs')
        self.connection = connection
        self.channel = channel
        self.exchange = exchange

    def emit(self, record):
        message = f"{record.levelname}: {record.msg}"
        self.channel.basic_publish(exchange=self.exchange, routing_key='logs', body=message)

    def close(self):
        try:
            self.connection.close()
        except AttributeError:
            pass
