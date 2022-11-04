from constants import *
from datetime import datetime
import os
import boto3

class DataHandler():
    def __init__(self):
        self.clients = [boto3.client('sqs'), boto3.client('s3')]

    def delete_expired_files(self, s3_bucket, s3_object, directory="/tmp"):
        kwargs = {"Bucket": s3_bucket, "Prefix": directory}
        
        response = self.clients[client_indices['s3']].list_objects_v2(**kwargs)
        for obj in response["Contents"]:
            if "." in obj["Key"]:
                key_date = datetime.now()
                last_modified = obj["LastModified"]
                if key_date - last_modified >= DURATION:
                    self.clients[client_indices['s3']].delete_object(Bucket=s3_bucket, Key=obj["Key"])
            
        return True