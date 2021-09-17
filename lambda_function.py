import boto3
import os
from boto3.dynamodb.conditions import Key
from datetime import datetime
import uuid

DYNAMO_BD = os.environ['DYNAMO_BD']

# Lore, aleja, walter, andres, geny, juand, juan, hernan, lucy, julian y toooooodos

class DynamoAccessor:
    def __init__(self, dynamo_table):
        dynamo_db = boto3.resource('dynamodb')
        self.table = dynamo_db.Table(dynamo_table)

    def get_data_from_dynamo(self, id):
        response = self.table.query(KeyConditionExpression=Key('id').eq(id))
        return response["Items"][0] if any(response["Items"]) else None

    def put_transaction(self, transaction):
        now = datetime.now()
        id = uuid.uuid1()
        response = self.table.put_item(
        Item={
                'id': id,
                'date': now,
                'transaction': transaction
            }
        )
        return response

def lambda_handler(event, context):
    dynamo_backend = DynamoAccessor(DYNAMO_BD)
    db_element = dynamo_backend.put_transaction(event['transaction'])
    return db_element

