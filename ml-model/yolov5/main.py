import subprocess
from subprocess import call, run
import json 
import pandas as pd
import os
import shutil
import boto3
import numpy as np
import cv2
import time
import sys
import PyPDF2
import pdf2image
from PIL import Image
import csv
import requests

PREPROCESS_FOLDER = "/home/ubuntu/MathSearch/ml-model/yolov5/preprocess_data/"
DATA_FOLDER = "/home/ubuntu/MathSearch/ml-model/yolov5/input_data/"

"""
pdf files location hard coded to DATA_FOLDER
Args: pdf_filename, target_filename

pdf_filename is inputs/[pdf_filename] of user's pdf query in S3's 'mathsearch-intermediary' bucket
target_filename is inputs/[target_file] of user's pdf query
"""

def main(pdf_image_prefix,local_target):
    """
    target_file_name: str of name of file we are looking for.
    Assumption: input_images/ has been updated with the latest images. 
    """
    print("running yolov5/main.py...")

    os.chdir("/home/ubuntu/MathSearch/ml-model/yolov5")
    target_file_name = local_target

    # Dataset contains output of YOLO model 
    # Clear folder to reset working directory 
    dataset_path = "ranking/dataset"
    if(os.path.isdir(dataset_path)):
      shutil.rmtree(dataset_path)

    # Call YOLO model. 
    # Uses best.torchscript weights 
    # Input data: input_data/
    # Writing output to ranking/dataset
    run('conda run -n pytorch python detect.py --weights best.torchscript --source input_data/{} --save-txt --save-crop --project ranking/dataset/'.format(sys.argv[1]), shell=True)

    # Get list of files written to YOLO output, except for target_file_name
    dir_list = os.listdir(os.path.join(dataset_path,"exp" ,"crops", "equation"))
    dir_list = [x for x in dir_list if x != target_file_name]

    # Construct tbl of generated crops for similarity detection model 
    img_database = pd.DataFrame(columns = ['image_name', 'image_source', 'coo_1', 'coo_2', 'coo_3', 'coo_4'])
    for f in dir_list:
      img_source, rem  = f.split("__")
      df = pd.read_csv(os.path.join(dataset_path,"exp" ,"labels/") + img_source + ".txt", delim_whitespace=True, header=None)
      new_row = {'image_name': f, 'image_source': img_source, 'coo_1':df.iloc[0, 1], 
          'coo_2':df.iloc[0, 2], 'coo_3': df.iloc[0, 3], 
          'coo_4': df.iloc[0, 4]} 
      img_database = img_database.append(new_row, ignore_index = True) 
    img_database.to_csv("ranking/img_database.csv") 

    # Call similarity detection model 
    # Writes final output to top5.csv
    run('conda run -n pytorch python ./ranking/ImageMatching.py',shell=True )


# Json example
# {
#  "file":"ex1.pdf",
#  "coords":"0 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698 1 0.32242063492063494 0.4380952380952381 0.26785714285714285 0.08888888888888889"
# }
def send_result_to_frontend(pdf_name):
    result_coords = ""
    result_csv = "/home/ubuntu/MathSearch/ml-model/yolov5/ranking/top5.csv"
    with open(result_csv, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            # adding page number and coords for each re-rank
            result_coords += str(int(row[0])+1) + " "

            # result_coords += row[0] + " "
            result_coords += row[3] + " "
            result_coords += row[4] + " "
            result_coords += row[5] + " "
            result_coords += row[6] + " "
    frontend_url = "http://3.94.25.91/api/result"
    json = {
        "file":pdf_name,
        "coords":result_coords
    }
    print(pdf_name)
    print(result_coords)
    res = requests.get(frontend_url, json=json)
    res = print(res) # OK = 200


def remove_files():
    global DATA_FOLDER
    for f in os.listdir(DATA_FOLDER):
        try:
            os.remove(os.path.join(DATA_FOLDER, f))
        except:
            shutil.rmtree(os.path.join(DATA_FOLDER, f)) 

def download_files(pdf_name, target_name):
    global DATA_FOLDER
    global PREPROCESS_FOLDER
    s3 = boto3.client("s3")
    MATHSEARCH_BUCKET='mathsearch-intermediary'
    local_pdf = PREPROCESS_FOLDER + pdf_name
    local_target = DATA_FOLDER + target_name[:-5] + "target.png"
    print("local_pdf",local_pdf)
    print("pdf_name",pdf_name)

    # download and preprocess pdf to png
    s3.download_file(
        Bucket=MATHSEARCH_BUCKET, Key="inputs/"+pdf_name, Filename=local_pdf
    )
    images = pdf2image.convert_from_path(local_pdf)
    print(local_pdf)
    os.mkdir(DATA_FOLDER + pdf_name)
    for i in range(len(images)):
        pdf_image = DATA_FOLDER + pdf_name + "/"+ str(i) + ".png"
        print(pdf_image)
        images[i].save(pdf_image)
    
    # download target png
    s3.download_file(
        Bucket=MATHSEARCH_BUCKET, Key="inputs/"+target_name, Filename=local_target
    )

if __name__ == "__main__":

    pdf_name = sys.argv[1]
    target_name = sys.argv[2]

    print(pdf_name)
    print(target_name)

    remove_files()
    time.sleep(5)
    download_files(pdf_name,target_name)

    # prefix example:
    # /home/ubuntu/MathSearch/ml-model/yolov5/input_data/012330fd-7c87-4236-8f4c-b39f3ea72968_pdf
    # actual path:
    # /home/ubuntu/MathSearch/ml-model/yolov5/input_data/012330fd-7c87-4236-8f4c-b39f3ea72968_pdf0.png
    pdf_image_prefix = DATA_FOLDER + pdf_name
    local_target = DATA_FOLDER + target_name[:-5] + "target.png"

    main(pdf_image_prefix,local_target)
    print("finished running yolo! sending results to frontend...")
    send_result_to_frontend(pdf_name)
