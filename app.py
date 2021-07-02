from os import O_EXLOCK
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename


from werkzeug.utils import redirect
from fourier import convert_to_fourier



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db= SQLAlchemy(app)



@app.route('/', methods = ['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/refresh', methods = ['POST'])
def refresh():
    file = request.files['file']
    convert_to_fourier("audio.wav")
    try:
        file.save('uploaded/wav_uploaded/en_cours/'+secure_filename(file.filename))
        # temp.convert_to_fourier('uploaded/wav_uploaded/en_cours/'+file.filename)
        return "Ok"
    except:
        return 'erreur enregistrement'

@app.route('/test',methods =['POST'])
def test():
    return "OK"
    
@app.route('/refresh2', methods = ['POST'])
def refresh2():
    print(request.files)
    
    return "a remplir"
    


@app.route('/refresh2', methods = ['POST'])
def refresh2():
    print(request.files)
    return "ok"
    


if __name__ == "__main__":
    app.run(debug=True)




