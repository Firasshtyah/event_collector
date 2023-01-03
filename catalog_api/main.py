import boto3
import json



s3 = boto3.resource('s3')

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def lambda_handler (event, context):

    product_id = event['queryStringParameters']['id']
    
    dydb = boto3.resource('dynamodb')
    table = dydb.Table('catalog_attr')
    response = table.get_item(Key={"product_id" :product_id},)

    clicks = response['Item']['clicks']

    response_body = {

        "product_id" : product_id,
        "clickcount" : clicks
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response_body, cls= JSONEncoder )
    }
