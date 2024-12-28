from cv2 import imread, resize
from numpy import expand_dims
from tensorflow.keras.saving import load_model
import pyrebase
import os
from dotenv import load_dotenv
import pika
from time import sleep
import json

load_dotenv()
MODEL_FILE='model.keras'
IMAGE_NAME='img.jpg'
QUEUE_NAME_RECEIVE = os.getenv("QUEUE_NAME_RECEIVE", "main")
QUEUE_NAME_MAIL = os.getenv("QUEUE_NAME_MAIL", "mail")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
CONFIG = {
    "apiKey": os.getenv("API_KEY"),
    "authDomain": "hand-gesture-recognition-test.firebaseapp.com",
    "projectId": "hand-gesture-recognition-test",
    "storageBucket": "hand-gesture-recognition-test.appspot.com",
    "messagingSenderId": "859385448146",
    "appId": "1:859385448146:web:ad4d2f80f15eb1ec24cf0b",
    "measurementId": "G-5LN3KZY65L",
    "databaseURL": ""
}

SUBJECT = 'Subject example'


firebase = pyrebase.initialize_app(CONFIG)
storage = firebase.storage()

model = load_model(MODEL_FILE)


# Functions
def download_image(cloud_image_name, local_image_name):
    storage.child(cloud_image_name).download('./', local_image_name)

def get_processed_image(fileName):
    img = imread(fileName)
    img = resize(img, (32, 32))
    return img/255.0

def predicate(imageName):
    predicate = model.predict(expand_dims(get_processed_image(imageName), axis=0))

    return predicate[0][0]


connection = None
channel = None

def connect(host):
    global connection
    global channel
    channel = None
    try:
        # lgr.debug(f'Connecting to {host}')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        channel = connection.channel()
    except Exception as e:
        # lgr.error(f'Error connecting to {host}: {e.args}')
        return None

    # lgr.info(f'Successfully connected to {host}')
    return channel

def send_to_mail(message):
    global channel
    if(channel == None):
        try:
            for i in range(5):
                channel = connect(RABBITMQ_HOST)
                
                if channel != None:
                    break
                sleep(5)
        except:
            print("error connection to RabbitMQ...")
        
    if(channel == None):
        print("cannot connect ot RabbitMQ")
        return False
    
    channel.basic_publish('', QUEUE_NAME_MAIL, message, properties=pika.BasicProperties(delivery_mode = pika.DeliveryMode.Persistent))

def callback(ch, method, properties, message):

    message_json = json.loads(message)

    img = message_json['image']
    download_image(img, IMAGE_NAME)

    predict = predicate(IMAGE_NAME)

    mail_dic = {'To': message_json['email'], 'Body': 'Your predict: ' + str(predict), 'Subject': SUBJECT}

    send_to_mail(json.dumps(mail_dic))
    
    ch.basic_ack(delivery_tag = method.delivery_tag)



def main():
    for i in range(5):
        channel = connect(RABBITMQ_HOST)
        
        if channel != None:
            break
        sleep(5)

    channel.queue_declare(queue=QUEUE_NAME_RECEIVE, durable=True)
    channel.basic_qos(prefetch_count=1)# will not sent more then 1 message to this service
    channel.queue_declare(queue=QUEUE_NAME_MAIL, durable=True)
    channel.basic_qos(prefetch_count=1)# will not sent more then 1 message to this service
    channel.basic_consume(queue=QUEUE_NAME_RECEIVE, on_message_callback=callback)

    channel.start_consuming()

if __name__ == '__main__':
    main()

#TODO:
# Change README file: add info about firebase
# Add logger