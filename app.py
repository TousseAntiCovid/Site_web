from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename


from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db= SQLAlchemy(app)



@app.route('/', methods = ['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/refresh', methods = ['POST'])
def refresh():
    file = request.files['file']

    try:
        file.save('wav_uploaded/en_cours'+secure_filename(file.filename))
        return "Le son à été enregistré"
    except:
        return "Il y a eu une ereur dans l'enregistrement"


@app.route('/refresh2', methods = ['POST'])
def refresh2():
    print(request.files)
    return "ok"
    


if __name__ == "__main__":
    app.run(debug=True)