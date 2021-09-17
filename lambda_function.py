import boto3
import os
from boto3.dynamodb.conditions import Key
import time
import uuid
import json

DYNAMO_BD = os.environ['DYNAMO_BD']

# Lore, aleja, walter, andres, geny, juand, juan, hernan, lucy, julian y toooooodos

class DynamoAccessor:
    def __init__(self, dynamo_table):
        dynamo_db = boto3.resource('dynamodb')
        self.table = dynamo_db.Table(dynamo_table)


    def put_transaction(self, transaction):
        ts = time.time()
        id = uuid.uuid4()
        response = self.table.put_item(
        Item={
                'id': str(id),
                'date': str(ts),
                'transaction': transaction
            }
        )
        return response

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Get the bucket name
    bucket = event['Records'][0]['s3']['bucket']['name']
    # Get the file from s3
    file_key_name = event['Records'][0]['s3']['object']['key']

    try:
        # Fecth the file from S3
        obj = s3.get_object(Bucket=bucket, Key=file_key_name)

        rows = obj['Body'].read().split(b'\n')

        for r in rows:
            print(r.decode())
            # email_content = email_content + '\n' + r.decode()

        # Parse and print the transactions
        # transactions = data['transactions']
        # for record in transactions:
        #     print(record['id'])
        #     print(record['date'])
        #     print(record['transaction'])
        # dynamo_backend = DynamoAccessor(DYNAMO_BD)
        # db_element = dynamo_backend.put_transaction(event['transaction'])
        return 'Success!'
    except Exception as e:
        print(e)
        raise e