import boto3
import json



s3 = boto3.resource('s3')

def lambda_handler (event, context):
    print(event['queryStringParameters']['id'])