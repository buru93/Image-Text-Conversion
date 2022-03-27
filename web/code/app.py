from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import os
from gtts import gTTS
from playsound import playsound
import requests

if os.environ.get('DOCKER', '') == "yes":
    UPLOAD_FOLDER = '/usr/src/app/images'
else:
    UPLOAD_FOLDER = 'images'


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template('home.html')


@app.route('/uploader', methods = ['POST', 'GET'])
def upload_file():
    NO_VALID_IMAGE = "No se ha proporcionado una imagen valida."
    if request.method == 'POST' and request.files:
        f = request.files['image']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        # img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        try:
            # text = pytesseract.image_to_string(img, "spa")
            ficheros = {'file': open(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)), 'rb')}
            url = "http://172.18.01:5050/uploadfile"
            text = requests.post(url, files=ficheros).json()['texto_imagen']
            
        except Exception as e:
            return render_template('results.html', text=e)
        
        if not os.environ.get('DOCKER', '') == "yes":
            myobj = gTTS(text=text, lang="es", slow=False)
            myobj.save(app.config['UPLOAD_FOLDER'] + "/speech.mp3")
            playsound(app.config['UPLOAD_FOLDER'] + "/speech.mp3")
        
        return render_template('results.html', text=text)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug = True)