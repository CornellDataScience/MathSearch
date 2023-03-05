client_indices = {
    'sqs': 0,
    's3': 1
}

# SQS
QUEUE_URL = 'MathSearchQueue-Input'
OUTPUT_QUEUE_URL = 'MathSearchQueue-Output'

# Duration before deletion
DURATION = 86400 * 7

# S3
BUCKET = 'mathsearch-intermediary'