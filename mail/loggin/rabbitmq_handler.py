from logging import Handler, LogRecord
import pika
from time import sleep

class RabbitMQHandler(Handler):
    def __init__(self, host, level: int | str = 0) -> None:
        super().__init__(level)
        
        self.connection = None
        self.channel = None

        for i in range(5):
            self.connect(host)
        
            if self.channel != None:
                break
            sleep(5)

    def connect(self, host):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
            self.channel = self.connection.channel()
        except Exception as e:
            return

        self.channel.queue_declare(queue='logs')

    def close_connect(self):
        self.connection.close()

    def send(self, message):
        self.channel.basic_publish(exchange='', routing_key='logs', body=message)

    def emit(self, record: LogRecord) -> None:
        self.send(self.format(record))

    def __del__(self):
        self.close()


# TODO: Refactor