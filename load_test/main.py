import boto3
import json
import random

firehose = boto3.client('firehose')

def lambda_handler (event, context):


    
    for i in range(50000):
        response = firehose.put_record(
            DeliveryStreamName="Events_recorder_stream",
                Record={
                    'Data': json.dumps(
                    {
                    "session_id" : str(random.randrange(1, 1000000)),
                    "creation_date" : "test",
                    "event_name" : "product_click",
                    "appCodeName" : "test",
                    "appName" : "test" ,
                    "userAgent" : "test",
                    "prodcut_id" : f"product_{str(random.randrange(1,1000))}"
                    }
                        )
                    
      
        }
        )