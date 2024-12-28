import sys
import os
import pika
from dotenv import load_dotenv
from time import sleep
import json

from loggin.loggin import config_logger
from mail_sender import MailSender

load_dotenv()

SENDER = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = os.getenv("QUEUE_NAME", "mail")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_HANDLERS = os.getenv("LOG_HANDLERS", ['file_handler', 'console_handler', 'rabbitmq_handler'])
LOG_FILENAME = os.getenv("LOG_FILENAME", 'logs/logs.log')

LOGGER = config_logger(LOG_LEVEL, LOG_HANDLERS, LOG_FILENAME, RABBITMQ_HOST)
MAIL_SENDER = MailSender(host=RABBITMQ_HOST)

CHANNEL = None

def connect(host):
    channel = None
    
    LOGGER.info(f'Connecting to {host}')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    LOGGER.info(f'Successfully connected to {host}')
    return channel

def connectToRabbitMQ():
    channel = None
    for i in range(5):
        try:
            channel = connect(RABBITMQ_HOST)
            return channel
        except Exception as e:
            LOGGER.error(f'Error connecting to {RABBITMQ_HOST}: {e.args}')
            sleep(5)
    raise ConnectionError("Cannot connect to the RabbitMQ")

def callback(ch, method, properties, message):

    message_json = json.loads(message)

    LOGGER.info('Processing a new message from queue')
    MAIL_SENDER.send(message_json['Subject'], message_json['Body'], SENDER, PASSWORD, message_json['To'])
    LOGGER.info('Confirming successfully sended message to RabbitMQ')
    ch.basic_ack(delivery_tag = method.delivery_tag)

def main():
    global CHANNEL

    LOGGER.info('Configuring mail service')
    CHANNEL = connectToRabbitMQ()

    LOGGER.debug('Decalrating queue')
    CHANNEL.queue_declare(queue=QUEUE_NAME, durable=True)
    LOGGER.debug('Configuring connection between mail sercice and RabbitMQ queue')
    CHANNEL.basic_qos(prefetch_count=1)# will not sent more then 1 message to this service
    LOGGER.debug('Configuring callback for RabbitMQ queue')
    CHANNEL.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    LOGGER.info('Service successfullt started and waiting for new messages')
    CHANNEL.start_consuming()


if __name__ == '__main__':
    main()
