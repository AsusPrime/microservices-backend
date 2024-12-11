import sys
import os
import pika
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from time import sleep
import json

from loggin.mail_loggin import config_logger

load_dotenv()

SENDER = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = os.getenv("QUEUE_NAME", "mail")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_HANDLERS = os.getenv("LOG_HANDLERS", ['file_handler', 'console_handler', 'rabbitmq_handler'])
LOG_FILENAME = os.getenv("LOG_FILENAME", 'logs/logs.log')

lgr = config_logger(LOG_LEVEL, LOG_HANDLERS, LOG_FILENAME, RABBITMQ_HOST)

def send(subject, body, sender, password, recipient):
    lgr.debug(f'Sending mail to {recipient}')
    if isinstance(body, bytes):
        lgr.debug('Decoding message')
        body = body.decode('utf-8')

    lgr.debug('Creating mail')
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipient, msg.as_string())

    lgr.info(f'Sended message to {recipient}')


def connect(host):
    channel = None
    try:
        lgr.debug(f'Connecting to {host}')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        channel = connection.channel()
    except Exception as e:
        lgr.error(f'Error connecting to {host}: {e.args}')
        return None

    lgr.info(f'Successfully connected to {host}')
    return channel

def callback(ch, method, properties, message):

    message_json = json.loads(message)

    lgr.info('Processing a new message from queue')
    send(message_json['Subject'], message_json['Body'], SENDER, PASSWORD, message_json['To'])
    lgr.debug('Confirming successfully sended message to RabbitMQ')
    ch.basic_ack(delivery_tag = method.delivery_tag)

def main():
    for i in range(5):
        channel = connect(RABBITMQ_HOST)
        
        if channel != None:
            break
        sleep(5)

    lgr.debug('Decalrating queue')
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    lgr.debug('Configuring connection between mail sercice and RabbitMQ queue')
    channel.basic_qos(prefetch_count=1)# will not sent more then 1 message to this service
    lgr.debug('Configuring callback for RabbitMQ queue')
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    lgr.info('Service successfullt started and waiting for new messages')
    channel.start_consuming()


if __name__ == '__main__':
    main()
