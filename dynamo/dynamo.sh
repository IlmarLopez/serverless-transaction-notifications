#!/bin/bash
aws cloudformation deploy \
--region us-west-1 \
--parameter-overrides DynamoName="lablambda" DynamoKey="dni" \
--stack-name dynamo-lambda-lab \
--template-file ./dynamo.yml