import os
import sox
from flask import Flask, flash, request, redirect, url_for, send_from_directory, after_this_request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './WorkingDirectory/'
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
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
        inputfilepath = os.path.join(app.config['UPLOAD_FOLDER'], 'inputFile.mp3')
        file.save(inputfilepath)    

        #Transformation
        tfm = sox.Transformer()
        if request.form.getlist('reverb'):
            tfm.reverb()
        if request.form.getlist('echo'):   
            tfm.echo()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        tfm.build(inputfilepath,filepath)
        
        @after_this_request
        def remove_file(response):
            try:
                os.remove(inputfilepath)
                #Can't remove the file because it's open, should work on linux server
                #os.remove(filepath)
            except Exception as error:
                app.logger.error("Error removing or closing downloaded file handle", error)
            return response      
        try:
            return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)
        except Exception as e:
            return str(e)
        
    
@app.route('/Form', methods=['GET'])
def return_form():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/" method=post enctype=multipart/form-data>
      reverb
      <input type=checkbox name=reverb>
      echo
      <input type=checkbox name=echo>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>'''

app.run()