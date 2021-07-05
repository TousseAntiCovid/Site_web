import os

#from app import app

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array

import numpy




def getModel(nom_model):
    model = load_model(nom_model)
    return model

def classifier(model,img):
    img = load_img(img, target_size=(336,336))
    img = numpy.asarray(img)
    img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
    y = model.predict(img)
    return str(y[0][0])

