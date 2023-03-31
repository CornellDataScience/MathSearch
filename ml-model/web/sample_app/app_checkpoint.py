from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, render_template
import urllib.request
import requests
import os
from flask import Flask
import wget

UPLOAD_FOLDER = '/home/ubuntu/yolov5/input_data'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def hello_world():
    return 'Warning: go to http://18.207.249.45/upload instead'

# https://www.cs.cornell.edu/~kozen/Papers/daa.pdf

@app.route('/pdf', methods=['GET', 'POST'])
def download():

    # url = request.args.get('c')
    # wget.download(url,app.config['UPLOAD_FOLDER']+"/file.pdf")


    # url = request.args.get('c')
    # print(url)
    # r = requests.get(url,allow_redirects=True)
    # print(r)
    # open(UPLOAD_FOLDER+"/file1.pdf","wb").write(r.content)


    # with open(app.config['UPLOAD_FOLDER']+"/file1.pdf", "wb") as file:
    #     response = requests.get(url)
    #     file.write(response.content)

    return "success"
    # return send_to_directory(app.config['UPLOAD_FOLDER'], link)
    # return send_file(link, as_attachment=True)


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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

if __name__ == "__main__":
    app.run()



# # from flask import Flask, render_template, request
# # # from werkzeug import secure_filename
# # from werkzeug.utils import secure_filename
# # from werkzeug.datastructures import  FileStorage
# # app = Flask(__name__)

# # @app.route('/')
# # def hello_world():
# #     return 'Hello World! - emerald@mathsearch port:3000 temp:4'

# # @app.route('/upload')
# # def upload_file():
# #    return render_template('upload.html')
	
# # @app.route('/uploader', methods = ['GET', 'POST'])
# # def uploadfile():
# #    if request.method == 'POST':
# #       f = request.files['file']
# #       f.save(secure_filename(f.filename))
# #       return 'file uploaded successfully'
		
# # if __name__ == '__main__':
# #     app.debug = True
# #     app.run(host='0.0.0.0', port=8100)


# from flask import Flask, flash, redirect, url_for, request, render_template
# from werkzeug.utils import secure_filename
# import os

# """
# @Author: Emerald Liu
# Does not support concurrency currently
# """

# # constant variables
# UPLOAD_FOLDER = '/home/ubuntu/yolov5/input_data'
# ALLOWED_EXTENSIONS = {'pdf'}

# # helper functions
# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# # initalize flask app config
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# # @app.route('/upload')
# # def upload_file():
# #    return render_template('upload.html')


# # @app.route('/upload', methods=['GET', 'POST'])
# # def upload_file():
# #     if request.method == 'POST':
# #         # check if the post request has the file part
# #         if 'file' not in request.files:
# #             flash('No file part')
# #             return redirect(request.url)
# #         file = request.files['file']
# #         # If the user does not select a file, the browser submits an
# #         # empty file without a filename.
# #         if file.filename == '':
# #             flash('No selected file')
# #             return redirect(request.url)
# #         if file and allowed_file(file.filename):
# #             filename = secure_filename(file.filename)
# #             # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# #             file.save(app.config['UPLOAD_FOLDER'], filename)
# #             return redirect(url_for('download_file', name=filename))
# #     return '''
# #     <!doctype html>
# #     <title>Upload new File</title>
# #     <h1>Upload new File</h1>
# #     <form method=post enctype=multipart/form-data>
# #       <input type=file name=file>
# #       <input type=submit value=Upload>
# #     </form>
# #     '''

# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=8100)


# import os
# import urllib.request
# # from app import app
# from flask import Flask, flash, request, redirect, render_template
# from werkzeug.utils import secure_filename

# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# app = Flask(__name__)

# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
# @app.route('/')
# def upload_form():
# 	return render_template('upload.html')

# @app.route('/', methods=['POST'])
# def upload_file():
# 	if request.method == 'POST':
#         # check if the post request has the file part
# 		if 'file' not in request.files:
# 			flash('No file part')
# 			return redirect(request.url)
# 		file = request.files['file']
# 		if file.filename == '':
# 			flash('No file selected for uploading')
# 			return redirect(request.url)
# 		if file and allowed_file(file.filename):
# 			filename = secure_filename(file.filename)
# 			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 			flash('File successfully uploaded')
# 			return redirect('/')
# 		else:
# 			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
# 			return redirect(request.url)

# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=8100)
