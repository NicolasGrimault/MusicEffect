import os
import sox
import transformerService
import uuid
from flask import Flask, flash, request, redirect, url_for, send_from_directory, after_this_request
from werkzeug.utils import secure_filename
from flasgger import Swagger, swag_from

UPLOAD_FOLDER = './WorkingDirectory/'
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])

app = Flask(__name__)
swagger = Swagger(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def prepareWorkingDirectory():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
@swag_from('effect.yml')
def transform_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        prepareWorkingDirectory()
        inputfilepath = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4())+'.mp3')
        file.save(inputfilepath)    

        #Transformation
        tfm = transformerService.getTransformer(request)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        tfm.build(inputfilepath,filepath)
        
        @after_this_request
        def remove_file(response):
            try:
                os.remove(inputfilepath)
                #Can't remove the file because it's open, should work on linux server
                os.remove(filepath)
            except Exception as error:
                app.logger.error("Error removing or closing downloaded file handle", error)
            return response      
        try:
            return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)
        except Exception as e:
            return str(e)

app.run()