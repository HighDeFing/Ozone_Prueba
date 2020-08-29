from flask import Flask, escape, request, redirect, render_template, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import shutil
import ntpath
from zipfile import ZipFile
import sys
from converter import gtlf2glb_call, obj2glb_call, fbx2glb_call
from pathlib import Path


UPLOAD_FOLDER = 'upload_files'  #folder of the uploads
ALLOWED_EXTENSIONS = {'gltf', 'glb', 'obj'}  #allowed_extensions still not aplicable
CONVERTED_FOLDER = 'converted_files'  #folder of the converted files
USER = 'generic_user_6' #user attribute and the name of the folder
UPLOAD_ID = "some_id" #this attribute is to differentiate between user uploads.



class upload_file_class:

    def __init__(self, files, type, user, upload_id):
        """
        :param file: A file type.
        :param type: type of 3D object.
        :param user: user_id.
        :param upload_id: id of the upload used to differentiate between user uploads.
        """
        self.files = files
        self.type = type
        self.user = user
        self.upload_id = upload_id
        self.source_file_path = "" #The source path.
        self.source_file_name = "" #The source only name of the glft, fbx, obj file.
        self.glb_path = "" #path of the glb final file.

    def save_file(self, save_folder):
        """
        :param save_folder: the path of the save folder
        :return:
        This method functions with normal folders
        """
        folder2create = self.user + self.upload_id
        path = os.path.join(save_folder, folder2create, self.type)
        if os.path.exists(path):  # creates a folder with user_id and replaces if it already exist
            shutil.rmtree(path)
        os.makedirs(path)
        #print("path_folder_created", path, file=sys.stderr)
        if self.type == 'obj':
            texture_path = os.path.join(path, 'textures')
            os.makedirs(texture_path)
        for f in self.files:
            if self.type == 'gltf' and (f.filename.endswith('.jpg') or f.filename.endswith('.png')):
                file_name = path_leaf(f.filename)
                file_path = os.path.join(path, file_name)
                f.save(file_path)
                # sometime gltf might have weird names in the texture files, since we can't change the gltf we accept the file name without secure_filename
                continue
            file_name = secure_filename(path_leaf(f.filename))
            #print("converted_path", file_name, file=sys.stderr)
            file_path = os.path.join(path, file_name)
            if file_name.endswith('.fbx'):
                self.source_file_path = file_path
                self.source_file_name = os.path.splitext(file_name)[0] # split text gets us the name without the extension
            if file_name.endswith('.gltf'):
                self.source_file_path = file_path
                self.source_file_name = os.path.splitext(file_name)[0]  # split text gets us the name without the extension
            if file_name.endswith('.obj'):
                self.source_file_path = file_path
                self.source_file_name = os.path.splitext(file_name)[0]  # split text gets us the name without the extension
            if self.type == 'obj' and (file_name.endswith('.jpg') or file_name.endswith('.png')):
                f.save(os.path.join(texture_path, file_name))
                continue #saves files in texture folder in upload of jpg and png textures
            f.save(file_path)
        return

    def save_file_zip(self, save_folder):
        """
        :param save_folder: the path of the save folder
        :return:
        This method functions with with zip folders
        """
        folder2create = self.user + self.upload_id
        path = os.path.join(save_folder, folder2create, self.type)
        if os.path.exists(path):  # creates a folder with user_id and replaces if it already exist
            shutil.rmtree(path)
        os.makedirs(path)
        path_name = path + '.zip' #add zip to the file path where is going to be saved
        self.files.save(path_name) #save the zip file
        unzip_files(path_name, path)  #unzip the file
        with os.scandir(path + '/') as entries:
            for entry in entries:
                for path_item in Path(entry).iterdir():
                    if path_item.is_file():
                        file_name = secure_filename(path_leaf(path_item)) #secure filename
                        file_path = path_item
                        if file_name.endswith('.obj'):
                            self.source_file_path = file_path
                            self.source_file_name = os.path.splitext(file_name)[0]
                        if file_name.endswith('.fbx'):
                            self.source_file_path = file_path
                            self.source_file_name = os.path.splitext(file_name)[0]  # split text gets us the name without the extension
                        if file_name.endswith('.gltf'):
                            self.source_file_path = file_path
                            self.source_file_name = os.path.splitext(file_name)[0]  # split text gets us the name without the extension

        #print(self.source_file_path, file=sys.stderr)
        #print(self.source_file_name, file=sys.stderr)

    def convert_file(self, converted_folder):
        converted_path = os.path.join(converted_folder, self.user, self.upload_id)  # Path of the converted folder and the user for that folder with id of the folder
        if os.path.exists(converted_path):  # creates a folder with user_id and replaces if it already exist
            shutil.rmtree(converted_path)
        os.makedirs(converted_path)
        if self.type == 'gltf':
            destination_path = converted_path + '/' + self.source_file_name + '.glb'  # Name of the new glb file
            #print("self.source_file_path", self.source_file_path, file=sys.stderr)
            #print("destination_path", destination_path, file=sys.stderr)
            gtlf2glb_call(self.source_file_path, destination_path)  # call to the converter
        if self.type == 'obj':
            destination_path = converted_path + '/' + self.source_file_name + '.glb'  # Name of the new glb file
            obj2glb_call(self.source_file_path, destination_path)  # call to the converter
        if self.type == 'fbx':
            destination_path = converted_path + '/' + self.source_file_name + '.glb'  # Name of the new glb file
            fbx2glb_call(self.source_file_path, destination_path)  # call to the converter
        self.glb_path = destination_path
        return



app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #when you do f.save this is where it ends.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
@app.route('/index.html')
def index():
    """
    Method for rendering upload.html
    :return:
    """
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_handle():
    """
    Method to handle the upload
    :return:
    """
    if request.method == 'POST':
        #files = request.files.getlist('file') #get the files in a File object
        type = request.form.get('category') #get the file type from the html
        #print(category, file=sys.stderr)
        file = request.files['file']
        user = USER
        upload_id = UPLOAD_ID
        my_upload = upload_file_class(file, type, user, upload_id)
        my_upload.save_file_zip(app.config['UPLOAD_FOLDER'])
        #my_upload.save_file(app.config['UPLOAD_FOLDER'])
        my_upload.convert_file(CONVERTED_FOLDER)
        # create_folder(files, user, type) #call the function to create the folder with the user name
    aux = os.path.join(CONVERTED_FOLDER, USER, UPLOAD_ID)
    complete_path = os.path.join(aux, os.listdir(aux)[0])
    filename = os.listdir(aux)[0]
    print(complete_path, file=sys.stderr)
    #return redirect(url_for('foo', complete_path=complete_path))
    return redirect(url_for('gallery'))


@app.route('/gallery.html')
@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    dirs = os.listdir(os.getcwd()+'\\converted_files')
    aux = os.path.join(CONVERTED_FOLDER, USER, UPLOAD_ID)
    complete_path = os.path.join(aux, os.listdir(aux)[0])
    return render_template('gallery.html', archivos=dirs, user=USER, complete_path=complete_path)


@app.route('/<path:complete_path>', methods=['GET', 'POST'])
def foo(complete_path):
    aux = os.path.join(CONVERTED_FOLDER, USER, UPLOAD_ID)
    filename = os.listdir(aux)[0]

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    dirs =os.listdir(os.getcwd()+'\\converted_files')
    return render_template('galeria.html', archivos=dirs)
    if os.path.exists("downloaded_files") == True:
            if len(os.listdir(os.getcwd()+'\\downloaded_files')) == 0:
                print("empty folder")
    else:
        os.mkdir ("downloaded_files")

    path_uploads= os.getcwd()+UPLOAD_FOLDER+'\\generic_user_6'
    path_downloads = os.getcwd()+'\\downloaded_files'

    my_file= open(path_uploads+'\\'+ filename,'r') 
    zip_files(path_uploads+'\\'+ filename, os.path.basename(filename) )
    my_file.close()

    shutil.move("file.zip", rutaDescargas)                  #move to the download folder

    my_file2 = open(path_downloads+ '\\'+ filename,'w')
    extrac_files(path_downloads)
    my_file2.close()
    return render_template('message_successful.html', MyFile = filename)

    #return 'this is the file {}'.format(filename)
    #return send_from_directory(aux, filename, as_attachment=True) #This is for download the file


# @app.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#     """
#     Method for handling the upload
#     :return: nothing
#     """
#     if request.method == 'POST':
#         #files = request.files.getlist('file') #get the files in a File object
#         type = request.form.get('category') #get the file type from the html
#         #print(category, file=sys.stderr)
#         file = request.files['file']
#         user = USER
#         upload_id = UPLOAD_ID
#         my_upload = upload_file_class(file, type, user, upload_id)
#         my_upload.save_file_zip(app.config['UPLOAD_FOLDER'])
#         #my_upload.save_file(app.config['UPLOAD_FOLDER'])
#         my_upload.convert_file(CONVERTED_FOLDER)
#         # create_folder(files, user, type) #call the function to create the folder with the user name
#         return 'file uploaded successfully'
#

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def unzip_files(files, into):
    with ZipFile(files, 'r') as zipObj:  # extras the file
        zipObj.extractall(into)

def zip_files(path,baseName):
    myzip = ZipFile("file.zip",'w')
    myzip.write (path, baseName) #search the folder downloaded_files
    myzip.close()

def extrac_files(path_file):
    with ZipFile(path_file+'\\file.zip','r') as myzip:           #extrac files from the zip
            myzip.extractall('downloaded_files')


def path_leaf(path):
    """
    :param path: Recives a path with a lot of '/'
    :return: Returns the only the name of the file without '/'
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


if __name__ == "__main__":
    """
    Run the code
    """
    #app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000, debug=True)

