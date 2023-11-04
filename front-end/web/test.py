import boto3

session = boto3.Session(profile_name='default')
s3_session = session.resource('s3')
bucket = s3_session.Bucket('mathsearch-intermediary')
for obj in bucket.objects.all():
   print(obj.key)