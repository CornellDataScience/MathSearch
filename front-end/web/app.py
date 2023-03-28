from flask import Flask

app = Flask(__name__)

@app.route('/render')
def hello_world():
	return 'Go Render Page :)'

if __name__ == "__main__":
	app.run()