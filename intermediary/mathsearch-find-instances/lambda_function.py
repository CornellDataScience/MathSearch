import urllib3
import json
import dataHandler
from constants import *
from botocore.vendored import requests

handler = dataHandler.DataHandler()
http = urllib3.PoolManager()

def lambda_handler(event, context):
    try:
        print("EVENT:" , event)
        print("CONTEXT:", context)
        
        # Extract message body
        #message_body = event['Records'][0]['body'] 
        message_body = handler.dequeue()
        print("Body: ", message_body)
        json_message = json.loads(message_body)
        pdf_path = json_message["pdf_path"]

        # PDF
        s3_bucket = BUCKET
        s3_pdf_object = '_'.join(pdf_path.split('_')[:-1])

        flask_endpoint = f"http://18.207.249.45/model?b={s3_bucket}&o={s3_pdf_object}"
        print("Flask endpoint: ", flask_endpoint)
        try:
            x = http.request('GET', flask_endpoint) #, params={"b": s3_bucket, "o": s3_pdf_object})
            print('AFTER GET', x)
        except Exception as e:
            print(e)
        print("Posted!")

        # Invoke model
        handler.invoke_model()
        print('AFTER MODEL')
        
        # Remove message from queue
        receipt_handler = event['Records'][0]['receiptHandle']
        response = boto3.client('sqs').delete_message(QueueUrl = QUEUE_URL, ReceiptHandle = receipt_handler)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully queried your document!'),
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps('Hello from Lambda!'),
            'error': e
        }