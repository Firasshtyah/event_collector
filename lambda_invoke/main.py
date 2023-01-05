import json
import boto3


client = boto3.client('lambda')

def lambda_handler(event, context):
    for i in range(0, 1000):
        url = 'url_{}'.format(i)
        
        response = client.invoke(
            FunctionName='events-recorder-LoadTest-zD8PlHKKqJGK',
            InvocationType='Event',
            Payload=json.dumps({'url': 'url_{}'.format(url)})
        )
        print(url)
        
    return