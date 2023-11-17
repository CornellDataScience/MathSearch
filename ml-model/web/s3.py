import boto3

# session = boto3.Session(profile_name='default')
# s3_session = session.resource('s3')
# bucket = s3_session.Bucket('mathsearch-intermediary')
# for obj in bucket.objects.all():
#    print(obj.key)

s3 = boto3.client("s3")
bucket_name='mathsearch-intermediary'
s3_file = 'test.txt'
local_file = '/home/ubuntu/MathSearch/ml-model/web/test.txt'
s3.download_file(
    Bucket=bucket_name, Key=s3_file, Filename=local_file
)
