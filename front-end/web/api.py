from flask import Flask, request, make_response, send_file
from flask_cors import CORS, cross_origin
import urllib.request
import requests
import subprocess
import time
import boto3

"""
Deploy flask. See https://github.com/CornellDataScience/MathSearch/blob/front-end/front-end/README.md
#! Be sure to add api/ prefix for flask deployment, root for react app only

"""

app = Flask(__name__)
CORS(app)
# app = Flask(__name__, static_folder='../mathsearch/build', static_url_path='/')

# curl -i -X GET -H "Content-Type: application/json" -d "{\"file\":\"012330fd-7c87-4236-8f4c-b39f3ea72968_pdf\",\"coords\":\"0 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698 1 0.32242063492063494 0.4380952380952381 0.26785714285714285 0.08888888888888889\"}" http://localhost:8001/api/result

# for frontend react to retrieve result from saved frontend EC2
# waits for backend to finish running model and return result
@app.route('/api/result')
def result():
	# start = time.time()
	data = request.json
	filename = data["file"]
	coords = data["coords"]
	venv_py = "/home/ubuntu/MathSearch/front-end/venv/bin/python3"
	python_file = "/home/ubuntu/MathSearch/front-end/web/render_result.py"
	info = "-f " + filename + " -c " + coords
	coords_lst = coords.split()
	page_lst = []

	MATHSEARCH_BUCKET='mathsearch-intermediary'
	local_pdf = "/home/ubuntu/MathSearch/front-end/web/pdf_in/" + filename
	s3 = boto3.client("s3")
	s3.download_file(
        Bucket=MATHSEARCH_BUCKET, Key="inputs/"+filename, Filename=local_pdf
    )
	subprocess.call([venv_py, python_file, info])
	for i in range(0,len(coords_lst),5):
		page_lst.append(int(coords_lst[i]))
	# json = {
	# 	"pdf":filename,
	# 	"pages":page_lst
	# }
	# end = time.time()
	return "done"

	#? broken code
	# with open('/home/ubuntu/MathSearch/front-end/web/pdf_out/'+filename, 'rb') as f:
	# 	pdf = f.read()
	# # pdf = "temp"
	# response_body = {
	# 	"pdf": pdf,
	# 	"pages": page_lst
	# }
	# print(response_body)
	# response = make_response(response_body)
	# response.headers['Content-Type'] = 'application/json'
	# time_str = "PDF saved! Time used: " + str(end - start)
	# return info+"\nresult page\n"+filename+"\n"+time_str+"\n"

# example
@app.route("/api/responsetest")
def example_response():
	pdf_file = 'pdf_out/ex1.pdf'
	# with open('pdf_out/ex1.pdf', 'rb') as f:
	# 	pdf = f.read()
	pages = [1, 2, 56]
	# response_body = {
	# 	"pdf": pdf,
	# 	"pages": pages
	# }
	# response = make_response(response_body)
	# response.headers['Content-Type'] = 'application/json'
	# return response
	return send_file(pdf_file, mimetype='application/pdf')

@app.route("/api/error")
def result_error():
	return "Error occurred during running of the model"

@app.route('/api/test')
def print_test_api():
	return "yesssssss the site is up - api/test\n"

@app.route('/test')
def print_test():
	print("called test")
	return "yesss! the site is up - update - debug - /test\n"

# not needed, handled by nginx now
# @app.route('/')
# def index():
#     return app.send_static_file('index.html')

if __name__ == "__main__":
	app.run(debug=True)