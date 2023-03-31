import subprocess
from subprocess import call
import json 
import pandas as pd
import os
import shutil
import boto3

# TODO this file is very bad right now. ML model team need to rewrite it.
# Please try use absolute path

def print_ok():
	return "importing ok\naccessing yolov5/main.py ok"

def main():
	"""
	target_file_name: str of name of file we are looking for.
	Assumption: input_images/ has been updated with the latest images. 
	"""
	print("running yolov5/main.py...")

	remove_files()
	download_files()
	
	target_file_name = get_source_target_name()

	# Dataset contains output of YOLO model 
	# Clear folder to reset working directory 
	dir = "/home/ubuntu/MathSearch/ml-model/yolov5/ranking/dataset/exp"
	shutil.rmtree(dir)
	# for f in os.listdir(dir):
	#    os.remove(os.path.join(dir, f)) 

	# Update target.json with target_file_name 
	os.remove("ranking/target.json")
	json_target_dict = {'name': target_file_name} 
	jsonString = json.dumps(json_target_dict)
	jsonFile = open("ranking/target.json", "w")
	jsonFile.write(jsonString)
	jsonFile.close()

	# Call YOLO model. 
	# Uses best.torchscript weights 
	# Input data: input_data/
	# Writing output to ranking/dataset
	call("./run_model.sh", shell=True)

	# Get list of files written to YOLO output, except for target_file_name
	dir_list = os.listdir(dir + "crops/equation/")
	print(dir_list) 
	dir_list = [x for x in dir_list if x != target_file_name]

	# Construct tbl of generated crops for similarity detection model 
	img_database = pd.DataFrame(columns = ['image_name', 'image_source', 'coo_1', 'coo_2', 'coo_3', 'coo_4'])

	for f in dir_list:
		img_source, rem  = f.split("__")
		eq_number = rem.split(".jpg")[0] 
		eq_number = 1 if eq_number == '' else eq_number
		
		df = pd.read_csv(dir + "labels/" + img_source + ".txt", delim_whitespace=True, header=None) 
		new_row = {'image_name': f, 'image_source': img_source, 'coo_1':df.iloc[int(eq_number) - 1, 1], 
				'coo_2':df.iloc[int(eq_number) - 1, 2], 'coo_3': df.iloc[int(eq_number) - 1, 3], 
				'coo_4': df.iloc[int(eq_number) - 1, 4]} 
		print(new_row)
		img_database = img_database.append(new_row, ignore_index = True) 

	img_database.to_csv("ranking/img_database.csv") 

	# Call similarity detection model 
	# Writes final output to top5.csv
	call("./ranking/run_image_matching.sh", shell=True) 
	
	# df = pd.read_csv("ranking/top5.csv") 
	# return df.to_json(orient="split")



# Below methods ML team do not need to worry, I will handle - Emerald

DATA_FOLDER = "/home/ubuntu/MathSearch/ml-model/yolov5/input_data"

def remove_files():
	global DATA_FOLDER
	for f in os.listdir(DATA_FOLDER):
		os.remove(os.path.join(DATA_FOLDER, f))

def save_file(s3_bucket,s3_object):
	global DATA_FOLDER
	file_name = s3_object.split('/')[-1]
	# boto3.client('s3').download_file(s3_bucket, s3_object, f'{DATA_FOLDER}/{file_name}')
	# TODO: accessing file not working, need to specify dir

INFO_FOLDER = "/home/ubuntu/MathSearch/ml-model/yolov5/input_info/"

def get_source_target_name():
	global INFO_FOLDER
	f = open(INFO_FOLDER+"names.txt")
	lines = f.read().splitlines()
	f.close()
	s3_object_pdf = lines[1]
	file_name = s3_object_pdf.split('/')[-1]+"_image"
	return file_name

def download_files():
	global DATA_FOLDER
	f = open(INFO_FOLDER+"names.txt") # Open file on read mode
	lines = f.read().splitlines() # List with stripped line-breaks
	f.close() # Close file
	print(lines)
	s3_bucket = lines[0]
	s3_object = lines[1]
	save_file(s3_bucket,s3_object+"_pdf")
	save_file(s3_bucket,s3_object+"_image")
