import json
import dataHandler
from constants import *

handler = dataHandler.DataHandler()

def lambda_handler(event, context):
    try:
        # TODO implement
        print("EVENT:" , event)
        print("CONTEXT:", context)
        
        # Extract message body
        message_body = handler.dequeue()
        print("Body: ", message_body)
        json_message = json.loads(message_body)
        pdf_path = json_message["path_to_pdf"]
        img_path = json_message["path_to_image"]

        print("Path to PDF: ", pdf_path)
        print("Path to image: ", img_path)

        # PDF
        pdf_slash_split = pdf_path.split('/')
        s3_bucket = pdf_slash_split[2]
        s3_object = '/'.join(pdf_slash_split[3:])
        
        print('S3 BUCKET: ', s3_bucket)
        print('S3 Object:', s3_object)

        file1 = handler.download_file_from_s3(s3_bucket, s3_object)

        # Image
        img_slash_split = img_path.split('/')
        s3_bucket = img_slash_split[2]
        s3_object = '/'.join(img_slash_split[3:])
        
        print('S3 BUCKET: ', s3_bucket)
        print('S3 Object:', s3_object)
        
        file2 = handler.download_file_from_s3(s3_bucket, s3_object)

        # Invoke model
        #handler.invoke_model(file1, file2)

        return_path = handler.upload_file_to_s3(s3_bucket, s3_object)
        
        # TODO: update to be the S3 info of the ML model's output
        current_message = {
            "path_output_image": return_path
        }
        handler.enqueue(OUTPUT_QUEUE_URL, json.dumps(current_message))
        
        # handler.download_file_from_s3('mathsearch-intermediary', 'mathsearch_test_pdf.png')
        # handler.upload_file_to_s3('mathsearch-intermediary', 'mathsearch_test_pdf.png')
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