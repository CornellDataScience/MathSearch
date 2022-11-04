from constants import *
from datetime import datetime
import os
import boto3

class DataHandler():
    def __init__(self):
        self.clients = [boto3.client('sqs'), boto3.client('s3')]
    
    def enqueue(self, message):
        self.clients[client_indices['sqs']].send_message(QueueUrl = queue_url, MessageBody = message)
    
    def dequeue(self):
        return self.clients[client_indices['sqs']].receive_message(QueueUrl = queue_url)['Messages']
    
    def invoke_model(self):
        pass

    def process_input(self, input):
        pass
    
    def format_output(self, output):
        pass

    def download_file_from_s3(self, s3_bucket, s3_object, directory="/tmp"):
        # s3 = boto3.resource('s3')
        # object = s3.Object('mathsearch-intermediary', 'mathsearch_test_pdf.png')
        # body = object.get()['Body'].read()
        # print(body)
        
        self.clients[client_indices['s3']].download_file(s3_bucket, s3_object, f'{directory}/mathsearch_{s3_object}')
        # with open("/tmp/tmpa.txt", "w") as f:
            # f.write('this is some content')
        
        print(os.listdir('/tmp'))
    
    def upload_file_to_s3(self, s3_bucket, s3_object, directory="/tmp"):
        self.clients[client_indices['s3']].upload_file(f'{directory}/mathsearch_{s3_object}', s3_bucket, f'{s3_object}_UPLOADED')
        
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