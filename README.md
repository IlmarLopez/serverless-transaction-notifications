# Notificaciones de transacciones - Serverless

## Despliegue del proyeto

### Pre-Requisitos

Desplegar todos los pre-requesitos para el proyecto, se desglosa en los siguiente:

- Buckets.
- Roles de pipeline.
- Llaves KMS. En este paso se deben desplegar primero el siguiente .sh [aws-codepipeline-prereq.sh](https://github.com/IlmarLopez/serverless-transaction-notifications/blob/main/prereq/aws-codepipeline-prereq.sh)
- Es recomendable crear una instancia de Cloud9 y se ejecute el aws-codepipeline-prereq.sh, este ejecutará el [template YML](https://github.com/IlmarLopez/serverless-transaction-notifications/blob/main/prereq/aws-codepipeline-prereq.yml) el cual desplegará todos los recursos neceserios de ahora en adelante para el proyecto.

### DynamoDB

Se debe realizar el despliegue de la BD DynamoDB en la que se almacenará el registro de los votantes con la siguiente informarción:

- ID
- Date
- Total balance
- Average debit amount
- Average credit amount
- Transactions

Esta BD se debe desplegar con el siguiente .sh [dynamo.sh](https://github.com/IlmarLopez/serverless-transaction-notifications/blob/main/dynamo/dynamo.sh) este ejecutará el [template YML](https://github.com/IlmarLopez/serverless-transaction-notifications/blob/main/dynamo/dynamo.yml). En este despliegue solo se crea la DynamoTable y DynamoKey.

### Pipeline y Lambda function

En este momento deplegar el pipeline que tendrá la función de automatizar el despliegue de nuestra serverless function.

1. **Estructura del repositorio** Se debe dejar la estructura del repositorio con el template.yml en la raíz y el código de la Lambda function también.

2. **Creación manual del Pipeline** Se debe usar CodePipeline para crear el pipeline siguiendo los siguientes pasos:

2.1 Crear el pipeline y seleccionar el role creado en los pre-requisitos.
![](../media/2.1.png?raw=true)
