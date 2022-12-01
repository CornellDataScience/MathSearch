"""
chmod 600 mathsearch-backend.pem
ssh -i "mathsearch-backend.pem" ubuntu@ec2-18-207-249-45.compute-1.amazonaws.com
"""

from flask import Flask, flash, redirect, url_for, request
# from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/home/ubuntu/yolov5/input_data'

# ALLOWED_EXTENSIONS = {'pdf'}

# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
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
        # if file and allowed_file(file.filename):
        if file:
            # filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
