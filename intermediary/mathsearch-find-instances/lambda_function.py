import json
import dataHandler
from constants import *

handler = dataHandler.DataHandler()

def lambda_handler(event, context):
    # TODO implement
    print("EVENT:" , event)
    print("CONTEXT:", context)
    
    sqs_body = handler.process_event(event)
    # TODO: extract S3 info from the sqs message body
    print('SQS Body:', sqs_body)
    
    # TODO: update to be the S3 info of the ML model's output
    handler.enqueue(output_queue_name, "new message from working lambda")
    
    # handler.download_file_from_s3('mathsearch-intermediary', 'mathsearch_test_pdf.png')
    # handler.upload_file_to_s3('mathsearch-intermediary', 'mathsearch_test_pdf.png')
    print("hi jason")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'test': json.dumps('Test')
    }
