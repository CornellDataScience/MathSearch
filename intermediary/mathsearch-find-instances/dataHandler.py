from constants import *
from datetime import datetime
import os
import boto3
import urllib3
from botocore.vendored import requests

class DataHandler():
    def __init__(self):
        self.clients = [boto3.client('sqs'), boto3.client('s3')]
        self.http = urllib3.PoolManager()
    
    def enqueue(self, queue_name, message):
        queue_url = self.clients[client_indices['sqs']].get_queue_url(QueueName = queue_name)['QueueUrl']
        self.clients[client_indices['sqs']].send_message(QueueUrl = queue_url, MessageBody = message)
    
    def dequeue(self):
        try:
            # Receive the message and parse the body
            received_message = self.clients[client_indices['sqs']].receive_message(QueueUrl = QUEUE_URL)
            body = received_message['Messages'][0]['Body']
            
            # Delete the corresponding message from the queue
            receipt_handler = received_message['Messages'][0]['ReceiptHandle']
            response = self.clients[client_indices['sqs']].delete_message(QueueUrl = QUEUE_URL, ReceiptHandle = receipt_handler)
            
            return body
        except Exception as e:
            print("Error: ", e)
    
    def invoke_model(self):
        self.http.request('GET', "http://18.207.249.45/run")

    def process_event(self, event):
        sqs_message = event['Records'][0]['body']
        
        return sqs_message
    
    def format_output(self, output):
        pass

    def download_file_from_s3(self, s3_bucket, s3_object, directory="/tmp"):
        file_name = s3_object.split('/')[-1]
        self.clients[client_indices['s3']].download_file(s3_bucket, s3_object, f'{directory}/mathsearch_{file_name}')        
        print(os.listdir('/tmp'))

        return file_name
        
    def get_object_url_from_s3(self, s3_bucket, s3_object, directory="/tmp"):
        file_name = s3_object.split('/')[-1]
        url_prefix = "https://mathsearch-intermediary.s3.amazonaws.com"
        self.clients[client_indices['s3']].download_file(s3_bucket, s3_object, f'{directory}/mathsearch_{file_name}')        
        print(os.listdir('/tmp'))

        return file_name
        
    def run(self):
        # Get new input
        message = self.dequeue()

        # Process the input
        self.process_input(message)

        # Invoke the model
        model_output = self.invoke_model()

        # Format the output
        output = self.format_output(model_output)
        
        # Return the output to the frontend
        return {'result': output}