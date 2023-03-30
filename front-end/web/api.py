from flask import Flask
import urllib.request
import requests


"""
Deploy flask. See https://github.com/CornellDataScience/MathSearch/blob/front-end/front-end/README.md
#! Be sure to add api/ prefix for flask deployment, root for react app only

"""

app = Flask(__name__)
# app = Flask(__name__, static_folder='../mathsearch/build', static_url_path='/')

# https://54.209.133.135/result?f=<filename>&c=<1 0.11 0.22 0.33 0.44 2 0.11 0.22 0.33 0.44>
# @app.route('/result', methods=['POST'])
@app.route('/api/result',methods=['POST'])
def result():
    filename = request.args.get('f')
    coords = request.args.get('c')
    return "result page\n"+filename+"\n"+coords

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