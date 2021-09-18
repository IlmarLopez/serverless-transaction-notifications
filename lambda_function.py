import boto3
import os
from boto3.dynamodb.conditions import Key
import time
import uuid

DYNAMO_BD = os.environ['DYNAMO_BD']

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
    # Get the bucket name
    bucket = event['Records'][0]['s3']['bucket']['name']
    # Get the file from s3
    file_key_name = event['Records'][0]['s3']['object']['key']

    try:
        s3 = boto3.client('s3')
        # dynamo_backend = DynamoAccessor(DYNAMO_BD)

        # Fecth the file from S3
        obj = s3.get_object(Bucket=bucket, Key=file_key_name)
        data = obj['Body'].read().decode('utf-8')
        
        print(data)

        transactions = data.split("\n")

        total_balance, pos_sum, neg_sum = 0.0, 0.0, 0.0
        pos_count, neg_count = 0, 0
        for r in transactions[1:]:
            r = r.split(",")
            amount = float(r[2])
            total_balance += amount
            if amount >= 0:
                pos_count += 1
                pos_sum += amount
            else:
                neg_count += 1
                neg_sum += amount

        average_credit_amount = round(float(pos_sum / pos_count), 2)
        average_debit_amount = round(float(neg_sum / neg_count), 2)

        print("Total balance ", total_balance)
        print("Average debit amount ", average_debit_amount)
        print("Average credit amount ", average_credit_amount)
        
        # db_element = dynamo_backend.put_transaction()
        
        # average_credit_amount = 0.0
        # average_debit_amount = 0.0
        return 'Success!'
    except Exception as e:
        print(e)
        raise e