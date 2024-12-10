from cv2 import imread, resize
from numpy import expand_dims
from tensorflow.keras.saving import load_model
import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()
MODEL_FILE='model.keras'
IMAGE_NAME='img.jpg'
CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
}

firebase = pyrebase.initialize_app(CONFIG)
storage = firebase.storage()

model = load_model(MODEL_FILE)


# Functions
def download_image(image_name):
    storage.child(image_name).download('./', IMAGE_NAME)

def get_processed_image():
    img = imread(IMAGE_NAME)
    img = resize(img, (32, 32))
    return img/255.0

def predicate():
    predicate = model.predict(expand_dims(get_processed_image, axis=0))

    return predicate[0][0]

download_image(IMAGE_NAME)

print("Succesfully downloaded")

#TODO:
# add rabbitqmq queue listener
# change image of python in docker file form default to 
#python with TF(also delete form requirements tf module)
# USE PYTHON 3.12 AS IMAGE FOR DOCKER!!!

# Change README file:
# * .env file(config for pyrebase)