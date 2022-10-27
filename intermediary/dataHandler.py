from constants import *
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

    def download_file_from_s3(self, s3_bucket, s3_object):
        self.clients[client_indices['s3']].download_file(s3_bucket, s3_object, f'mathsearch_{s3_object}')

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