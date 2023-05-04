import subprocess
from subprocess import call
import json 
import pandas as pd
import os
import shutil
import boto3
import numpy as np
import cv2
import time

DATA_FOLDER = "/home/ubuntu/MathSearch/ml-model/yolov5/input_data"
INFO_FOLDER = "/home/ubuntu/MathSearch/ml-model/yolov5/input_info/"
TARGET_FILE_LOC = "/home/ubuntu/MathSearch/ml-model/yolov5/ranking/target.json"
aws_access_key_id='AKIAUHGY3PCBKOGUKOJN'
aws_secret_access_key='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'

def main():
    """
    target_file_name: str of name of file we are looking for.
    Assumption: input_images/ has been updated with the latest images. 
    """
    print("running yolov5/main.py...")

    # download input files
    remove_files()
    download_files(bucket='mathsearch-intermediary', subfolder='ex01/', img_format='png')

    os.chdir("/home/ubuntu/MathSearch/ml-model/yolov5")
    target_file_name = get_source_target_name()
    # print(target_file_name)
    # assert 1 == 0

    # Dataset contains output of YOLO model 
    # Clear folder to reset working directory 
    dataset_path = "ranking/dataset"
    # target_file = "ranking/target.json"
    # if(os.path.isdir(dataset_path)):
    #   shutil.rmtree(dataset_path)
    
    # # Update target.json with target_file_name 
    # if(os.path.exists(target_file)):
    #   os.remove(target_file)
    # json_target_dict = {'name': target_file_name} 
    # jsonString = json.dumps(json_target_dict)
    # jsonFile = open(target_file, "w")
    # jsonFile.write(jsonString)
    # jsonFile.close()

    # Call YOLO model. 
    # Uses best.torchscript weights 
    # Input data: input_data/
    # Writing output to ranking/dataset
    call("conda activate pytorch", shell=True)
    call("bash run_model.sh", shell=True)  

    

    # Get list of files written to YOLO output, except for target_file_name
    # print("1")
    # time.sleep(7) # TODO
    # print("dl", os.path.join(dataset_path, "exp","crops", "equation"))

    dir_list = os.listdir(os.path.join(dataset_path,"exp" ,"crops", "equation"))
    
    dir_list = [x for x in dir_list if x != target_file_name]

    # Construct tbl of generated crops for similarity detection model 
    img_database = pd.DataFrame(columns = ['image_name', 'image_source', 'coo_1', 'coo_2', 'coo_3', 'coo_4'])

    for f in dir_list:
      img_source, rem  = f.split("__")
      # eq_number = rem.split(".png")[0] 
      # eq_number = 1 if eq_number == '' else eq_number
      
      # df = pd.read_csv(os.path.join(dataset_path,"exp" ,"labels/") + img_source + ".txt", delim_whitespace=True, header=None) 
      # new_row = {'image_name': f, 'image_source': img_source, 'coo_1':df.iloc[int(eq_number) - 1, 1], 
      #     'coo_2':df.iloc[int(eq_number) - 1, 2], 'coo_3': df.iloc[int(eq_number) - 1, 3], 
      #     'coo_4': df.iloc[int(eq_number) - 1, 4]} 
      # print(img_source)
      # print(eq_number)
      # print(img_source)
      df = pd.read_csv(os.path.join(dataset_path,"exp" ,"labels/") + img_source + ".txt", delim_whitespace=True, header=None)
      new_row = {'image_name': f, 'image_source': img_source, 'coo_1':df.iloc[0, 1], 
          'coo_2':df.iloc[0, 2], 'coo_3': df.iloc[0, 3], 
          'coo_4': df.iloc[0, 4]} 
      img_database = img_database.append(new_row, ignore_index = True) 

    img_database.to_csv("ranking/img_database.csv") 

    # Call similarity detection model 
    # Writes final output to top5.csv
    call("./ranking/run_image_matching.sh", shell=True) 


def remove_files():
    global DATA_FOLDER
    for f in os.listdir(DATA_FOLDER):
      os.remove(os.path.join(DATA_FOLDER, f))

def save_file(s3_bucket,s3_object):
    global DATA_FOLDER
    file_name = s3_object.split('/')[-1]
    boto3.client('s3').download_file(s3_bucket, s3_object, f'{DATA_FOLDER}/{file_name}')

def download_files(bucket, subfolder, img_format):
    global INFO_FOLDER
    global DATA_FOLDER
    global aws_access_key_id
    global aws_secret_access_key

    prefix = subfolder
    mybucket = bucket

    f = open(INFO_FOLDER+"names.txt") # Open file on read mode
    lines = f.read().splitlines() # List with stripped line-breaks
    f.close() 

    mybucket = lines[0]
    prefix = lines[1]

    # TODO read from config file
    s3 = boto3.client(service_name='s3', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    for obj in s3.list_objects(Bucket=mybucket, Prefix=prefix).get('Contents'):
      k = obj.get('Key')
      if k[-3:] != img_format:
        continue
      file_name = obj.get('Key').split('/')[-1]
      s3.download_file(Bucket=mybucket,Key=k, Filename=f'{DATA_FOLDER}/{file_name}')

def get_source_target_name():
	# global INFO_FOLDER
	f = open(TARGET_FILE_LOC)
	lines = f.read().splitlines()
	f.close()
	target = lines[1]
	# file_name = s3_object_pdf.split('/')[-1]+"_image"
	return target

if __name__ == "__main__":
  main()