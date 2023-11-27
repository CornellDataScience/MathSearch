from constants import *
#from datetime import datetime
#import os
import boto3
import urllib3
#from botocore.vendored import requests

class DataHandler():
    def __init__(self):
        self.clients = [boto3.client('sqs'), boto3.client('s3')]
        self.http = urllib3.PoolManager()
    
    def list_s3_objects(self, bucket_name):
        s3 = boto3.client("s3")
        response = s3.list_objects_v2(Bucket=bucket_name)
        return response.get('Contents', [])
    
    def extract_uuid(self, file_name):
        return file_name[7:-4]
    
    def delete_sqs_message(self, queue_url, receipt_handle):
        sqs = boto3.client('sqs')
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        
    def is_expected_image_present(self, objects, expected_image):
        for object in objects:
            if expected_image in object['Key']:
                return True
        return False