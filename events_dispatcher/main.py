import boto3
import json



s3 = boto3.resource('s3')

def lambda_handler (event, context):
    apps = ['catalog','insider']
    bucket_name = event["Records"][0]['s3']['bucket']['name']
    src_key = event["Records"][0]['s3']['object']['key']
    object_src = {
    'Bucket': bucket_name,
    'Key': src_key
        }
    print(bucket_name)
    print(src_key)
    dest_file_name = src_key.split('/')[-1]

    
    for app in apps :
        dest_key = f'apps/{app}/{dest_file_name}'
        print(dest_key)
        s3.meta.client.copy(object_src,bucket_name, dest_key)