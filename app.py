from os import O_EXLOCK
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
import sounddevice as sd
from scipy.io.wavfile import write

from werkzeug.utils import redirect
from fourier import convert_to_fourier
from model import getModel, classifier

import random
import string
import os
import multiprocessing
import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



def find_number():
    file = os.listdir('uploaded/wav_uploaded/en_cours/')
    number_files = len(file)
    return number_files

def fourier(filename):
    while os.path.exists("uploaded/fourrier_uploaded/en_cours/"+filename) == False :
        conversion = multiprocessing.Process(None,convert_to_fourier,args=(filename[:-4]+".wav",))
        conversion.start()
        time.sleep(30)
        print ("Process")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/refresh', methods=['POST'])
def refresh():
    #Récupere le fichier dans la requete
    file = request.files['file']

    # Renomme le fichier
    comp = find_number()
    filename = "uploaded_" + str (comp) + ".wav" #Filename audio
    file_entire = 'uploaded/wav_uploaded/en_cours/' + filename # Filename audio avec path 

    filename_png = str(filename[:-4]+".png") #FIlename image
    
    #Enregistrement de l'audio
    file.save(file_entire)
    
    #Transformée de fourier
    fourier(filename_png)
    model = getModel("model_336")
    rep = classifier(model,"uploaded/fourrier_uploaded/en_cours/"+filename_png)
    if int(float(rep)) < 0.1:
        return "covid"
    if int(float(rep)) > 0.9:
        return "Non-covid"
    else:
        return "Non défini"



@app.route('/test', methods=['POST'])
def test():
    fs = 44100 
    seconds = 7  
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait() 
    comp = find_number()
    file = "uploaded/wav_uploaded/en_cours/recorded_"+ str(comp)+ ".wav"
    write(file, fs, myrecording)
    fourier("recorded_"+str(comp)+".png")
    model = getModel("model_336")
    rep = classifier(model,"uploaded/fourrier_uploaded/en_cours/"+"recorded_"+str(comp)+".png")
    if int(float(rep)) < 0.1:
        return "covid"
    if int(float(rep)) > 0.9:
        return "Non-covid"
    else:
        return "Non défini"

    
    
@app.route('/refresh2', methods = ['POST'])
def refresh2():
    print(request.files)
    
    return "a remplir"
    


if __name__ == "__main__":
    app.run(debug=True)




