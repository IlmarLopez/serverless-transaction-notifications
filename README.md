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
![Create pipeline](../media/2.1.png?raw=true)

2.2 Agregar como source el repositorio en GitHub y autorizar la aplicación. Seleccionar el repositorio y la branch.
![Add source stage](../media/2.2.png?raw=true)

2.3 Agregar Codebuild como fase.
![Codebuild como fase](../media/2.3.png?raw=true)

2.4 Crear proyecto de Codebuild.
![Create proyect with Codebuild](../media/2.4.png?raw=true)

2.5 Seleccionar la imagen del contenedor que se ejecutará en el Codebuild y también el role de codebuild creado en los pre-requisitos atenriormente.
![Environment](../media/2.5.png?raw=true)

2.6 Setear como variable de entorno el bucket creado en pre-requisitos.
![Environment variables](../media/2.6.png?raw=true)

2.7 Especificar la ruta del buildspec que estara en la carpeta config del repo.
![Environment variables](../media/2.7.png?raw=true)

2.8 Agregar etapa de implementación (create or update change set), las capabilities especificadas, seleccionar el role de Cloudformation (crear role en caso de no existir).
![Add deploy stage](../media/2.8.png?raw=true)

2.9 Guardar y posteriormente editar el pipeline.
![Create or update change set](../media/2.9.png?raw=true)

2.10 Editar fase (Edit: Deploy)
![Edit deploy fase](../media/2.10.png?raw=true)

2.11 La tarea debe ser de tipo execute change set quien desplegará el cambio en la lambda.
![Edit action - execute change set](../media/2.11.png?raw=true)

De ahora en adelante el pipe se ejecutará cuando el repositorio en su rama main reciba un push que disparará el webhook.

### Asignar Lambda función al Bucket S3

3.1 Selecionar el bucket storitransactionsbucket creado en los pre-requisitos anteriormente.
![Bucket storitransactionsbucket](../media/3.1.png?raw=true)

3.2 Crear evento de notificación en la sección de propiedades del Bucket
![Bucket storitransactionsbucket](../media/3.2.png?raw=true)

3.3 Seleccionar el tipo evento y la función Lambda.
![Bucket storitransactionsbucket](../media/3.3.png?raw=true)

3.4 Subur un documento con el siguiente formato de [txns.csv](../src/txns.csv?raw=true) al bucket. Esto va a disparar el llamado de la fucnión Lambda.
![storitransactionsbucket Upload](../media/3.4.png?raw=true)

3.4 Debe llegar un email con el siguiente formato.
![email](../media/3.5.png?raw=true)

Y por último revisar la base de datos para verificar que los registros fueron guardados correctamente.
![email](../media/3.6.png?raw=true)
