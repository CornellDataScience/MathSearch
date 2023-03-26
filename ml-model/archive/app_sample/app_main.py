from flask import Flask, flash, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import os

"""
@Author: Emerald Liu
Does not support concurrency currently
"""

# constant variables
UPLOAD_FOLDER = '/home/ubuntu/yolov5/input_data'
ALLOWED_EXTENSIONS = {'pdf'}

# helper functions


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# initalize flask app config
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route('/upload')
# def upload_file():
#    return render_template('upload.html')

@app.route('/')
def hello_world():
    return 'Hello World! - emerald@mathsearch port:3000 temp:1'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
