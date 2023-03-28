from flask import Flask
import urllib.request
import requests

app = Flask(__name__)

# http://18.207.249.45/render?f=<filename>&c=<1 0.11 0.22 0.33 0.44 2 0.11 0.22 0.33 0.44>
@app.route('/render', methods=['POST'])
def redner():
    filename = request.args.get('f')
    coords = request.args.get('c')

if __name__ == "__main__":
	app.run(debug=True)