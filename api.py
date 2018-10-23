import os
import sox
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = './TempFiles/'
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            tempfilepath = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.mp3')
            file.save(tempfilepath)    
            tfm = sox.Transformer()
            if request.form.getlist('reverb'):
                tfm.reverb()
            if request.form.getlist('echo'):   
                tfm.echo()
            tfm.build(tempfilepath,filepath)

            os.remove(tempfilepath)
            try:
                return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)
            except Exception as e:
                return str(e)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      reverb
      <input type=checkbox name=reverb>
      echo
      <input type=checkbox name=echo>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

app.run()