import re
import base64
import numpy as np
import io
from io import BytesIO
from PIL import Image
import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import request
from flask import jsonify
from flask import Flask

app = Flask(__name__)

def get_model():
    global model
    model = load_model('C:/Users/Saud K/Downloads/projectwork/model.h5')
    print(" * Model loaded!")

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    #image = image.resize(target_size)
    image = img_to_array(image)
    image = [np.expand_dims(image, axis=0)]

    return np.vstack(image)

print(" * Loading Keras model...")
get_model()

@app.route("/predict", methods=["POST"])
def predict():
    #byteImgIO = io.BytesIO()
    message = request.get_json(force=True)
    encoded = message['image']
    #message=request.json
    #image_data = (message)
    #pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
    #decoded=base64.decodestring(encoded)
    decoded =base64.b64decode(encoded)
    #ii=io.BytesIO(decoded)

    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(2000, 2000))
    x = processed_image.astype('float32')/255
    x_test=np.array(x[int(len(x) * (1 - 0.2)):])
    prediction = model.predict(x_test).tolist()

    response = {
        'prediction': {
            'A': prediction[0][0],
            'B': prediction[0][1],
            'C': prediction[0][2]
            #'dog': prediction[0],
            #'cat': prediction[1]
        }
    }
    return jsonify(response)