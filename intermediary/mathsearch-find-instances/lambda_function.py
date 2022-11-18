import json
import dataHandler
from constants import *

handler = dataHandler.DataHandler()

def lambda_handler(event, context):
    # TODO implement
    print("EVENT:" , event)
    print("CONTEXT:", context)
    
    # Extract message body
    message_body = handler.dequeue()
    print("Body: ", message_body)
    
    # TODO: extract S3 info from the sqs message body
    
    # TODO: update to be the S3 info of the ML model's output
    current_message = "TODO: model output"
    handler.enqueue(OUTPUT_QUEUE_URL, current_message)
    
    # handler.download_file_from_s3('mathsearch-intermediary', 'mathsearch_test_pdf.png')
    # handler.upload_file_to_s3('mathsearch-intermediary', 'mathsearch_test_pdf.png')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'test': json.dumps('Test')
    }
