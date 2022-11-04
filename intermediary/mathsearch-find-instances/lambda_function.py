import json
import dataHandler

handler = dataHandler.DataHandler()

def lambda_handler(event, context):
    # TODO implement
    print(event)
    print(context)
    print("hello")
    print("bob")
    print("dsafdsafdsaf")
    handler.download_file_from_s3('mathsearch-intermediary', 'mathsearch_test_pdf.png')
    handler.upload_file_to_s3('mathsearch-intermediary', 'mathsearch_test_pdf.png')
    print("hi jason")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'test': json.dumps('Test')
    }
