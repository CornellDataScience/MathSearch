"""

@author: Emerald Liu

1. Test deploy
http://44.192.0.110/test

2. Run machine learning model
http://44.192.0.110/run
{
   "uuid":"uuidKey1",
   "pdf_path":"inputs/a0eeed5e-1d18-42ff-a347-878785830dc0_pdf",
   "image_path":"inputs/a0eeed5e-1d18-42ff-a347-878785830dc0_image"
}

"""

from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, render_template
import urllib.request
import requests
import os
import json
import sys
import time
import subprocess
from subprocess import call
import shutil
# import pandas as pd
# import boto3

UPLOAD_FOLDER = '/home/ubuntu/yolov5/input_data'

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	# response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
	return response

@app.route('/')
def start():
	return 'visit:\nhttp://18.207.249.45/coord\nhttp://18.207.249.45/model\n\noptional:\nhttp://18.207.249.45/upload'

# https://www.cs.cornell.edu/~kozen/Papers/daa.pdf


# @app.route('/coord', methods=['GET'])
# def get_coord():
# 	f = open('/home/ubuntu/yolov5/ranking/top5.txt', "r")
# 	return f.read()


@app.route('/model', methods=['GET', 'POST'])
def download():
	s3_bucket = request.args.get('b')
	s3_object = request.args.get('o')
	with open("/home/ubuntu/yolov5/input_info/names.txt", "w") as f:
		f.write(s3_bucket+"\n"+s3_object)
	return s3_bucket+"\n"+s3_object+"\nPassed data info successfully!"


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

@app.route('/test')
def print_test():
	return "ok-update 5/6"

@app.route('/run', methods=['POST'])
def run_model():
	print("/run called")
	data = request.json
	uuid = data["uuid"]
	print("before",data["pdf_path"])
	print("before",data["image_path"])
	pdf_path = data["pdf_path"][7:]
	image_path = data["image_path"][7:]
	print(pdf_path)
	print(image_path)
	message = uuid + " " + pdf_path + " " + image_path
	# import time
	# os.chdir('/home/ubuntu/yolov5')
	# sys.path.append('/home/ubuntu/yolov5')
	# import main
	# main.main()
	# time.sleep(3)
	# return "running model...\n\nVisit:\nhttp://18.207.249.45/coord\nhttp://18.207.249.45/model\n\noptional:\nhttp://18.207.249.45/upload"
	start = time.time()
	# venv_py = "/home/ubuntu/MathSearch/ml-model/venv/bin/python3"
	venv_py = "/opt/conda/bin/python3"
	python_file = "/home/ubuntu/MathSearch/ml-model/yolov5/main.py"
	subprocess.call([venv_py, python_file, pdf_path, image_path])
	end = time.time()
	return message + "\nimporting ok\naccessing yolov5/main.py ok" + "\n" + "ML model finished running.\nTime used: " + str(end - start)


if __name__ == "__main__":
	app.run(debug=True)
