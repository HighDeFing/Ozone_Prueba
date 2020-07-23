from flask import Flask, escape, request, redirect, render_template, flash, url_for
from werkzeug.utils import secure_filename
import sys
import os
from pygltflib import GLTF2

UPLOAD_FOLDER = 'upload_archives'
ALLOWED_EXTENSIONS = {'gltf', 'glb', 'obj'}
CONVERTED_FOLDER = 'converted_files'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/upload.html', methods=['GET', 'POST'])
def hello():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        file_name = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        convert_gltf_to_glb(file_name)
        return 'file uploaded successfully'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_gltf_to_glb(f):
    gltf = GLTF2().load(f)
    print(f, file=sys.stderr)
    gltf.save(os.path.join(CONVERTED_FOLDER, "test.glb"))


if __name__ == "__main__":
    #app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000, debug=True)

