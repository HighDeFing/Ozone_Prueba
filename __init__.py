from flask import Flask, escape, request, redirect, render_template, flash, url_for
from werkzeug.utils import secure_filename
import sys
import os
import shutil
import ntpath
from os import walk
from pygltflib import GLTF2
from converter import gtlf2glb_call, obj2glb_call


UPLOAD_FOLDER = 'upload_archives'
ALLOWED_EXTENSIONS = {'gltf', 'glb', 'obj'}
CONVERTED_FOLDER = 'converted_files'
USER = 'generic_user'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/upload.html', methods=['GET', 'POST'])
def hello():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    """
    Method for handling the upload
    :return: nothing
    """
    if request.method == 'POST':
        files = request.files.getlist('file')
        type = request.form.get('category') #get the file type
        #print(category, file=sys.stderr)
        user = USER
        create_folder(files, user, type)
        # f = request.files['file']
        # file_name = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        # convert_gltf_to_glb(file_name)
        return 'file uploaded successfully'


def create_folder(files, user, type):
    """
    :param files: Recibes a file.type form request.files.getlist() this is a method from multiple  webkitdirectory
    :param user: user name
    :param type: file archive type
    :return: nothing

    This fuction create a folder with the user param as name in upload_achives, and saves the files in it.
    """
    path = os.path.join(app.config['UPLOAD_FOLDER'], user, type)
    if os.path.exists(path): #creates a folder with user_id and replaces if it already exist
        shutil.rmtree(path)
    os.makedirs(path)
    for f in files:
        file_name = secure_filename(path_leaf(f.filename))
        #print("converted_path", file_name, file=sys.stderr)
        file_path = os.path.join(path, file_name)
        if file_name.endswith('.gltf'):
            source_file_path = file_path
            source_file_name = os.path.splitext(file_name)[0]
        if file_name.endswith('.obj'):
            source_file_path = file_path
            source_file_name = os.path.splitext(file_name)[0]
        f.save(file_path)
    converted_path = os.path.join(CONVERTED_FOLDER, user)  # Path of the converted folder and the user for that folder
    # print("converted_path", converted_path, file=sys.stderr)
    # print("gltf_file_path", gltf_file_path, file=sys.stderr)
    if os.path.exists(converted_path):  # creates a folder with user_id and replaces if it already exist
        shutil.rmtree(converted_path)
    os.makedirs(converted_path)
    if type == 'gltf':
        destination_path = converted_path + '/' + source_file_name + '.glb' #Name of the new glb file
        gtlf2glb_call(source_file_path, destination_path) #call to the converter
    if type == 'obj':
        destination_path = converted_path + '/' + source_file_name + '.glb'  # Name of the new glb file
        obj2glb_call(source_file_path, destination_path)  # call to the converter



def path_leaf(path):
    """
    :param path: Recives a path with a lot of '/'
    :return: Returns the only the name of the file without '/'
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# def upload_files():
#     if request.method == 'POST':
#         f = request.files['file']
#         file_name = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
#         f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
#         convert_gltf_to_glb(file_name)
#         return 'file uploaded successfully'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    """
    Run the code
    """
    #app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000, debug=True)

