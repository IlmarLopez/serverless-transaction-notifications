import boto3
import os
from boto3.dynamodb.conditions import Key
import time
import uuid
from datetime import datetime
import calendar
from botocore.exceptions import ClientError
from botocore.vendored import requests

DYNAMO_BD = os.environ['DYNAMO_BD']

# Process an list of records returning the total records per month - format date "M/DD".
def total_by_month(date_list):
    months_with_total = {}
    for date in date_list:
        month_name = calendar.month_name[date.month]
        if month_name not in months_with_total:
            months_with_total[month_name] = 1
        else:
            months_with_total[month_name] += 1
    return months_with_total

class DynamoAccessor:
    def __init__(self, dynamo_table):
        dynamo_db = boto3.resource('dynamodb')
        self.table = dynamo_db.Table(dynamo_table)

    def put_account_statement(self, statement, txns_list):
        ts = time.time()
        id = uuid.uuid4()
        response = self.table.put_item(
        Item={
                'id': str(id),
                'date': str(ts),
                'totalBalance': str(statement.get("total_balance")),
                'averageDebitAmount': str(statement.get("average_debit_amount")),
                'averageCreditAmount': str(statement.get("average_credit_amount")),
                "transactions": txns_list
            }
        )
        return response

def send_email(source, destination, account_statement, total_transactions_by_month):
    ses_client = boto3.client("ses", region_name="us-west-1")
    CHARSET = "UTF-8"
   
    BODY_HTML = """
        <table cellspacing="0" cellpadding="0" width="100%" style="margin:0; padding:0; width:100%">
          <!-- GRADIENT SECTION -->
          <tr>
            <td width="100%" style="padding:0; margin:0;">
              <div style="padding: 5px" style="background-color: #85EBB1; background: linear-gradient(to right bottom,#2cd5c4,#bdffa1);">
                <img src="https://blog.storicard.com/wp-content/uploads/2019/07/stori.logo-horizontal-03.png" width="160"
                  height="63" alt="logo-stori">
              </div>
              <center>
        
                <table cellspacing="0" cellpadding="0" border="0" width="650" style="margin:0; padding:0; width:650px" align="center" class="mobile-full-table">
                  <tr>
                    <td>
                        <h4 style="margin-bottom: 2px">Summary:</h4>
                        <ul>
    """
    
    # Set data from account statement
    BODY_HTML += "<li>Total balance: <strong>$ {}</strong>.</li>".format(account_statement.get("total_balance"))
    BODY_HTML += "<li>Average debit amount: <strong>$ {}</strong>.</li>".format(account_statement.get("average_debit_amount"))
    BODY_HTML += "<li>Average credit amount: <strong>$ {}</strong>.</li>".format(account_statement.get("average_credit_amount"))

    BODY_HTML += "</ul>"
    BODY_HTML += "<h5 style=\"margin-bottom: 2px\">Number of transactions by month:</h5>"
    BODY_HTML += "<ul style=\"list-style-type: none; margin: 5px 0; padding: 0;\">"

    for k, v in total_transactions_by_month.items():
        BODY_HTML += "<li>Number of transactions in {} :  <strong>{}</strong></li>".format(k, str(v))

    BODY_HTML += """
                        </ul>
                        <!-- MAIN CTA Goes here -->
                    </td>
                  </tr>
                </table>
              </center>
            </td>
          </tr>
          <!-- GRADIENT SECTION - ENDS-->
          <tr>
            <td>
                <!-- OTHER EMAIL CONTENT -->
                <center>
                    <div style="width: 650px; margin-top: 2em;">
                        <small>
                            Para dudas o aclaraciones, comun??cate al (55) 7822 6649 las 24hrs del d??a, los 365 d??as del a??o o escribe a nuestra ??rea de servicio, 
                            Stori Contigo al correo 
                            <a href="mailto:storicontigo@storicard.com" target="_blank">
                                <span>storicontigo@storicard.com</span>
                            </a>
                        </small>
                    </div>
                </center>
            </td>
          </tr>
        </table>
    """
    
    ses_client.send_email(
        Destination={
            "ToAddresses": [
                destination,
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": BODY_HTML,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Account statement",
            },
        },
        Source=source,
    )

def lambda_handler(event, context):
    try:
        # Get the bucket name
        bucket = event['Records'][0]['s3']['bucket']['name']

        # Get the file from s3
        file_key_name = event['Records'][0]['s3']['object']['key']

        s3 = boto3.client('s3')
        dynamo_backend = DynamoAccessor(DYNAMO_BD)

        # Fecth the file from S3
        obj = s3.get_object(Bucket=bucket, Key=file_key_name)
        data = obj['Body'].read().decode('utf-8')

        transactions = data.split("\n")

        txns_list = []
        date_list = []
        total_balance, pos_sum, neg_sum = 0.0, 0.0, 0.0
        pos_count, neg_count = 0, 0
        for r in transactions[1:]:
            r = r.split(",")
            id_str = str(r[0])
            date_str = r[1]
            date = datetime.strptime(date_str, '%m/%d')
            amount = float(r[2])
            total_balance += amount
            if amount >= 0:
                pos_count += 1
                pos_sum += amount
            else:
                neg_count += 1
                neg_sum += amount

            txns = {"id" : id_str, "date" : date_str, "amount": str(amount)}
            txns_list.append(txns)
            date_list.append(date)

        average_credit_amount = round(float(pos_sum / pos_count), 2)
        average_debit_amount = round(float(neg_sum / neg_count), 2)

        account_statement = {
            "total_balance": total_balance,
            "average_debit_amount": average_debit_amount,
            "average_credit_amount": average_credit_amount
        }
        
        dynamo_backend.put_account_statement(account_statement, txns_list)

        total_transactions_by_month = total_by_month(date_list)
        send_email("ilmarfranciscol@gmail.com", "ilmarlopezr@hotmail.com", account_statement, total_transactions_by_month)
        return 'Success!'
    except Exception as e:
        print(e)
        raise e
        