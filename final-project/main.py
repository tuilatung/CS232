import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath

app = Flask(__name__, template_folder='templates')
app.secret_key = "super secret key"
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('home.html')


@app.route("/getimage")
def get_img():
    return "compressed_animal1.jpg"

if __name__ == "__main__":
    app.debug = True
    app.run()