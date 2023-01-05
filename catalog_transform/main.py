import json
import boto3
from botocore.exceptions import ClientError

unique_list = []

def product_list(events_count):
 
    for x in events_count:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

def lambda_handler(event, context):
    
    
    dydb = boto3.resource('dynamodb')
    table = dydb.Table('catalog_attr')

    
    bucket_name = event["Records"][0]['s3']['bucket']['name']
    src_key = event["Records"][0]['s3']['object']['key']
    

    s3 = boto3.client('s3')
    events_object = s3.get_object(Bucket=bucket_name, Key=src_key)
    events_object_content = events_object['Body'].read().decode('utf-8')
    events_json = events_object_content.replace('}{','},{')
    events_json = f"[{events_json}]"
    events_list = json.loads(events_json)
    events_count=[]

        
    for event in events_list :
        events_count.append(event['prodcut_id'])
        
    product_list(events_count)
    for product in unique_list:
        
        print(f"{product}:{events_count.count(product)}")

        try:
            response = table.get_item(Key={"product_id" :product},)
            
            prodcut_id = response['Item']['product_id']
            
            
            response_update = table.update_item(
                    Key={
                        'product_id': prodcut_id
                    },
                    UpdateExpression='SET clicks = :clicks',
                    ExpressionAttributeValues={
                        ':clicks': response['Item']['clicks']+events_count.count(product)
                    },
                    ReturnValues="UPDATED_NEW"
                    )
            
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            print("throttle")
            print(error_code)
            if error_code == 'ProvisionedThroughputExceededException':
                print(e)
    
        except Exception as e:
            print("not created")
            print(e)
            response = table.put_item(
                    Item={
                'product_id': product,
                'clicks' : 0}
                    )
            response = table.get_item(Key={"product_id" :product},)
            
            prodcut_id = response['Item']['product_id']
            
            
            response_update = table.update_item(
                    Key={
                        'product_id': prodcut_id
                    },
                    UpdateExpression='SET clicks = :clicks',
                    ExpressionAttributeValues={
                        ':clicks': response['Item']['clicks']+events_count.count(product)
                    },
                    ReturnValues="UPDATED_NEW"
                    )
    print(src_key)