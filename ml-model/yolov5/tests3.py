import boto3
from botocore.config import Config
import cv2
import numpy as np

s3 = boto3.client(service_name='s3', region_name='us-east-1', aws_access_key_id='AKIAUHGY3PCBKOGUKOJN', aws_secret_access_key='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')
# s3 = boto3.resource('s3')
mybucket = 'mathsearch-intermediary'
prefix = 'ex01/'

i = 0
for obj in s3.list_objects(Bucket=mybucket, Prefix=prefix).get('Contents'):
  k = obj.get('Key')
  if k[-3:] != 'png':
    continue
  contents = s3.get_object(Bucket=mybucket,Key=obj.get('Key'))['Body'].read()
  print(cv2.imdecode(np.asarray(bytearray(contents)), cv2.IMREAD_COLOR))
  # print(contents)
  # contents = obj.get()['Body'].read()
#   if contents != None and contents != "b''":
#     print("contents:",contents,'end')
#     print(cv2.imdecode(np.asarray(bytearray(contents)), cv2.IMREAD_COLOR))
  # i += 1
  # if i > 2:
  #   break
# bucket = s3.Bucket('mathsearch-intermediary')
# for obj_sum in bucket.objects.all():
  # obj = s3.Object(obj_sum.bucket_name, obj_sum.key)
  # cv.imshow(obj_sum.get()['Body'].read())
  # cv2.imshow(obj)