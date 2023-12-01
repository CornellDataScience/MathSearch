client_indices = {
    'sqs': 0,
    's3': 1
}

# SQS
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/290365077634/MathSearchSQS'
OUTPUT_BUCKET = 'mathsearch-outputs'
# OUTPUT_QUEUE_URL = 'MathSearchQueue-Output'

# Duration before deletion
DURATION = 86400 * 7

# S3
BUCKET = 'mathsearch-intermediary'