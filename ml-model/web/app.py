"""

Author: Emerald Liu

Deployed flask on ec2
ip: 18.207.249.45
Use url as commands to control flask.

Commands:
1. http://18.207.249.45/coord [GET]
Get best matching equation page number and bonding box coordinates.
Return object see /home/ubuntu/yolov5/main.py

2. http://18.207.249.45/model?b=$s3_bucket$&o=$s3_object$ [POST]
Post target image and candidate pdf file to ec2.
Inputs: s3_bucket, s3_object without _png or _image postfix
Sample usage: http://18.207.249.45/model?b=mathsearch-intermediary&o=inputs/2dd62a75-0f22-4121-9bb7-22085cfda77f

3. http://18.207.249.45/upload [POST]
Backup option to upload input data to ec2.

4. http://18.207.249.45/run [POST]
Run model at /home/ubuntu/yolov5/main.py.

"""


from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, render_template
import urllib.request
import requests
import os
import json
import sys

import subprocess
from subprocess import call
import shutil
# import pandas as pd
# import boto3

UPLOAD_FOLDER = '/home/ubuntu/yolov5/input_data'

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'visit:\nhttp://18.207.249.45/coord\nhttp://18.207.249.45/model\n\noptional:\nhttp://18.207.249.45/upload'

# https://www.cs.cornell.edu/~kozen/Papers/daa.pdf

@app.route('/coord', methods=['GET'])
def get_coord():
    f = open('/home/ubuntu/yolov5/ranking/top5.txt', "r")
    return f.read()


@app.route('/model', methods=['GET','POST'])
def download():
    s3_bucket = request.args.get('b')
    s3_object_pdf = request.args.get('o')
    s3_object_img = s3_object_pdf[:-3]+"img"
    with open("/home/ubuntu/yolov5/input_info/names.txt", "w") as f:
        f.write(s3_bucket+"\n"+s3_object_pdf+"\n"+s3_object_img)
    return s3_bucket+"\n"+s3_object_pdf+"\n"+s3_object_img+"\nPassed data info successfully!"


ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


@app.route('/run')
def dynamic_page():
    import time
    os.chdir('/home/ubuntu/yolov5')
    sys.path.append('/home/ubuntu/yolov5')
    import main
    main.main()
    time.sleep(3)
    return "running model...\n\nVisit:\nhttp://18.207.249.45/coord\nhttp://18.207.249.45/model\n\noptional:\nhttp://18.207.249.45/upload"

if __name__ == "__main__":
    app.run(debug = True)

    