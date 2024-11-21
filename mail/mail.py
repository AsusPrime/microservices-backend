import sys
import os
import pika
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
import time

load_dotenv()

QUEUE_NAME = 'main'
SENDER = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send(subject, body, sender, password, recipient):
    if isinstance(body, bytes):
        body = body.decode('utf-8')

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipient, msg.as_string())

    print('Message sent!')

def connect(host):
    channel = None
    try:
        print(f'Connecting to {host}...')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        channel = connection.channel()
    except Exception as e:
        print(f'Error connecting to {host}: {e}')
        return None

    return channel

def getMessage(rabbitmq_host, queue_name, callback):
    for i in range(5):
        channel = connect(rabbitmq_host)
        
        if channel != None:
            break
        time.sleep(5)

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def parse_message(message):
    return []

if __name__ == '__main__':
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    if(RABBITMQ_HOST == None or RABBITMQ_HOST == ""):
        print('environment RABBITMQ_HOST not set', file=sys.stderr)
        exit()
    
    getMessage(RABBITMQ_HOST, QUEUE_NAME, lambda ch, method, properties, body: send('subject', body, SENDER, PASSWORD, SENDER))
