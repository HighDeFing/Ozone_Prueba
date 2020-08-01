from flask import Flask, escape, request, redirect, render_template, flash, url_for
from werkzeug.utils import secure_filename
import os
import shutil
import ntpath
from converter import gtlf2glb_call, obj2glb_call


UPLOAD_FOLDER = 'upload_files'  #folder of the uploads
ALLOWED_EXTENSIONS = {'gltf', 'glb', 'obj'}  #allowed_extensions still not aplicable
CONVERTED_FOLDER = 'converted_files'  #folder of the converted files
USER = 'generic_user' #user attribute and the name of the folder

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #when you do f.save this is where it ends.


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
        files = request.files.getlist('file') #get the files in a File object
        type = request.form.get('category') #get the file type from the html
        #print(category, file=sys.stderr)
        user = USER
        create_folder(files, user, type) #call the function to create the folder with the user name
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
            source_file_name = os.path.splitext(file_name)[0] #split text gets us the name without the extension
        if file_name.endswith('.obj'):
            source_file_path = file_path
            source_file_name = os.path.splitext(file_name)[0] #split text gets us the name without the extension
        f.save(file_path) #this saves the original file in the upload_files folder.
    converted_path = os.path.join(CONVERTED_FOLDER, user)  # Path of the converted folder and the user for that folder
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    """
    Run the code
    """
    #app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000, debug=True)

