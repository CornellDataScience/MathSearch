# import subprocess
# from subprocess import call
# import json 
# import pandas as pd
# import os
# import shutil

#! /usr/bin/env python
#! /bin/bash
echo "I ran this"
echo "more lines"

# import boto3

# UPLOAD_FOLDER = '/home/ubuntu/yolov5/input_data'

# f = open('/home/ubuntu/yolov5/input_info/names.txt') # Open file on read mode
# lines = f.read().splitlines() # List with stripped line-breaks
# f.close() # Close file

# def save_file(s3_bucket,s3_object):
# 	file_name = s3_object.split('/')[-1]
# 	boto3.client('s3').download_file(s3_bucket, s3_object, f'{UPLOAD_FOLDER}/{file_name}')

# s3_bucket = lines[0]
# s3_object_pdf = lines[1]
# s3_object_img = lines[2]
# print(s3_bucket,s3_object_pdf)
# print(s3_bucket,s3_object_img)
# save_file(s3_bucket,s3_object_pdf)
# save_file(s3_bucket,s3_object_img)
