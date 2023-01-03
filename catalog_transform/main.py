import json
import boto3


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

        
    for event in events_list :
        
 

        try:
            response = table.get_item(Key={"product_id" :event['prodcut_id']},)
            
            prodcut_id = response['Item']['product_id']
            
            print(prodcut_id)
            
            response_update = table.update_item(
                    Key={
                        'product_id': prodcut_id
                    },
                    UpdateExpression='SET clicks = :clicks',
                    ExpressionAttributeValues={
                        ':clicks': response['Item']['clicks']+1
                    },
                    ReturnValues="UPDATED_NEW"
                    )
            print(response_update)
            
            
        except Exception as e:
            response = table.put_item(
                            Item={
                        'product_id': event['prodcut_id'],
                        'clicks': 1
                         }
                )
            print(response)

    #         # insider_event = {
                
    #         #     'creation_date' : json.dumps(event_dict['creation_date']),
    #         #     'sid' : event_dict['session_id'] ,
    #         #     'source' : event_dict['appCodeName'] ,
    #         #     'url' : event_dict['URL'],
    #         #     'product_id' : event_dict['prodcut_id'],
    #         #     'userAgent': event_dict['userAgent']
    #         # }
    #         # insider_event_list.append(insider_event)
    #     # bucket_name = "vogatransform"
    #     # file_name = f"insider_batch_{context.aws_request_id}"
    #     # s3_path = "insider/" + file_name
    #     # s3.put_object(Bucket=bucket_name,Key=s3_path, Body=json.dumps(insider_event_list))
    #     # print(insider_event_list[0])
            

    # except Exception as e: 
    #     print(e)