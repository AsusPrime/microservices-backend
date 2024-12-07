import pika
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()




TOKEN = os.getenv('TOKEN')

def callback(ch, method, properties, body):
    log_message = body.decode()
    print('message:', log_message)

def connect():
    print('connecting...')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    print('declarating queue...')
    channel.queue_declare(queue='logs')

    channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)

    print('starting consuming...')
    channel.start_consuming()
    


def start_rabbitmq_listener():
    for i in range(5):
        try:
            connect()
        except Exception as e:
            print('failed to connect...')
            sleep(5)
            continue
        break


def main():
    pass


if __name__ == '__main__':
    main()



# TODO: add logging
# Refactor
# REMOVE API!!!
# Change saving id's from file to DB
# Add bot