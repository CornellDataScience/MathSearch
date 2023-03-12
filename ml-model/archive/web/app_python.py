import sys
import pandas
import os
sys.path.append('/home/ubuntu/yolov5')
import main


def remove_files(data_dir):
	for f in os.listdir(data_dir):
		os.remove(os.path.join(data_dir, f))

if __name__ == "__main__":

	# clear data dir
	data_dir = '/home/ubuntu/yolov5/input_data'
	# remove_files(data_dir)

	# run flask to download files
    # app.run()

	target_search = "target_search.png"
	target_file = "/home/ubuntu/yolov5/input_data/sample_doc.pdf"

	os.chdir('/home/ubuntu/yolov5')
	main.main(target_search)

	# return stuff