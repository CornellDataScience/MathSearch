import json
import dataHandler

handler = dataHandler.DataHandler()

def lambda_handler(event, context):
    # TODO implement
    print(event)
    print(context)
    handler.delete_expired_files('mathsearch-intermediary')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'test': json.dumps('Test')
    }
