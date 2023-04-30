from flask import Flask, request, make_response
import urllib.request
import requests
import subprocess
import time

"""
Deploy flask. See https://github.com/CornellDataScience/MathSearch/blob/front-end/front-end/README.md
#! Be sure to add api/ prefix for flask deployment, root for react app only

"""

app = Flask(__name__)
# app = Flask(__name__, static_folder='../mathsearch/build', static_url_path='/')

# file = ex1.pdf
# coords = 0 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698 1 0.32242063492063494 0.4380952380952381 0.26785714285714285 0.08888888888888889
# https://54.209.133.135/api/result
@app.route('/api/result')
def result():
	start = time.time()
	data = request.json
	filename = data["file"]
	coords = data["coords"]
	venv_py = "/home/ubuntu/MathSearch/front-end/venv/bin/python3"
	python_file = "/home/ubuntu/MathSearch/front-end/web/render_result.py"
	info = "-f " + filename + " -c " + coords
	# subprocess.call([venv_py, python_file, info])
	end = time.time()
	time_str = "PDF saved! Time used: " + str(end - start)
	return info+"\nresult page\n"+filename+"\n"+coords+"\n"+time_str+"\n"

@app.route("/api/responsetest")
def example_response():
	response_body = {
		"pdf": "hello",
		"pages": [1,2,3]
	}
	response = make_response(response_body)
	response.headers['Content-Type'] = 'application/json'
	return response

@app.route("/api/error")
def result_error():
	return "Error occurred during running of the model"

@app.route('/api/test')
def print_test_api():
	return "yes the site is up - api/test"

@app.route('/test')
def print_test():
	return "yes the site is up - /test"

# not needed, handled by nginx now
# @app.route('/')
# def index():
#     return app.send_static_file('index.html')

if __name__ == "__main__":
	app.run(debug=True)