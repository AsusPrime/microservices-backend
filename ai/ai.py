from cv2 import imread, resize
from numpy import expand_dims
from tensorflow.keras.saving import load_model
import pyrebase

MODEL_FILE='model.keras'
IMAGE_NAME='img.jpg'

config = {
    "apiKey": "AIzaSyCK8ViLcr36fvQoYxd2YM15bxazTUBWxmU",
    "authDomain": "hand-gesture-recognition-test.firebaseapp.com",
    "projectId": "hand-gesture-recognition-test",
    "storageBucket": "hand-gesture-recognition-test.appspot.com",
    "messagingSenderId": "859385448146",
    "appId": "1:859385448146:web:ad4d2f80f15eb1ec24cf0b",
    "measurementId": "G-5LN3KZY65L"
}

firebase = firebase.initialize_app(config)
storage = firebase.storage()

model = load_model(MODEL_FILE)


# Functions
def download_image(image_name):
    storage.child(image_name).download(IMAGE_NAME)

def get_processed_image():
    img = imread(IMAGE_NAME)
    img = resize(img, (32, 32))
    return img/255.0

def predicate():
    predicate = model.predict(expand_dims(get_processed_image, axis=0))

    return predicate[0][0]


#TODO:
# add rabbitqmq queue listener
# change image of python in docker file form default to 
#python with TF(also delete form requirements tf module)
