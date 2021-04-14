from botocore.client import Config
from chalice import Chalice
import json
import boto3
import os
import sys
import uuid
import time
from boto3.dynamodb.conditions import Key, Attr

app = Chalice(app_name='fileUpload')

FILE_UPLOAD_BUCKET = "Enter bucket name"


@app.route('/')
def index():
    return {'method': "index"}


####################################################################################################################################
# file uploader
####################################################################################################################################

@app.route('/presignpost', cors=True
           )
def upload():
    s3_client = boto3.client(
        's3', 'eu-west-2', config=Config(s3={'addressing_style': 'path'}))

    filename = str(app.current_request.query_params.get('filename'))
    filesize = app.current_request.query_params.get('filesize')
    key = str(uuid.uuid1()) + "/" + filename

    fields = {
        "Content-Type": str(app.current_request.query_params.get('filetype'))}
    resp = s3_client.generate_presigned_post(
        Bucket=FILE_UPLOAD_BUCKET,
        Key=key,
        Fields=fields,
    )

    metadata = getMetaValues(
        app.current_request.query_params.get('expiry'), filename, filesize)
    downloadUrl = getRandomUrl()
    dynamoresp = createDynamoItem(downloadUrl, key, metadata)
    return getResponsupload(200, resp, downloadUrl, "success")


def getResponsupload(statusCode, key, url, status):
    body = {'key': key, 'downloadlink': url, 'status': status}
    return {
        'statusCode': statusCode,
        'headers': {"Access-Control-Allow-Origin": "*"},
        'body': json.dumps(body),
        'isBase64Encoded': False,
    }


def getRandomUrl():
    return str(uuid.uuid4())[:8]


def createDynamoItem(url, key, metadata):
    dynamodbclient = boto3.resource('dynamodb')
    table = dynamodbclient.Table('fileuploadlookup')
    resp = table.put_item(
        Item={
            'uri': url,
            's3file': key,
            'metadata': {
                "burnafterread": metadata['burnafterread'],
                "deleted": False,
                "expiry": int(metadata['expiry']),
                "filename": metadata['filename'],
                "filesize": metadata['filesize']
            },

        }
    )
    return resp


def getMetaValues(expiry, filename, filesize):

    if expiry == '1':
        return {'burnafterread': True, 'expiry': time.time() + ((60 * 60) * 24) * 7, 'filename': filename, 'filesize': filesize}
    elif expiry == '2':
        return {'burnafterread': False, 'expiry': time.time() + (60 * 30), 'filename': filename, 'filesize': filesize}
    elif expiry == '3':
        return {'burnafterread': False, 'expiry': time.time() + (60 * 60) * 24, 'filename': filename, 'filesize': filesize}
    elif expiry == '4':
        return {'burnafterread': False, 'expiry': time.time() + ((60 * 60) * 24) * 7, 'filename': filename, 'filesize': filesize}
    else:
        return {'burnafterread': True, 'expiry': time.time() + ((60 * 60) * 24) * 7, 'filename': filename, 'filesize': filesize}


####################################################################################################################################

# File downloader

####################################################################################################################################


@app.route('/get/{item}', cors=True)
def get(item):
    pathParameters = item
    print(item)
    path = item
    s3Bucket = FILE_UPLOAD_BUCKET

    # #validate item exists else error
    dbItem = getDynamoItem(path)
    print("DBITEM = {}".format(dbItem))

    if dbItem != False:
        # item found in dynomodb
        preSignedKey = getS3PreSignedURL(s3Bucket, dbItem['s3file'])
        print("preSignedKey = {}".format(preSignedKey))
        if preSignedKey != False:
            # key generated
            if dbItem['metadata']['deleted'] == False and float(dbItem['metadata']['expiry']) > float(time.time()):
                if dbItem['metadata']['burnafterread'] == True:
                    setItemMetadata(path, "deleted", True)
                # return metadata file name, file size

                return getResponse(200, preSignedKey, dbItem['metadata']['filename'], dbItem['metadata']['filesize'], 'success')
            else:
                setItemMetadata(path, "deleted", True)
                return getResponse(404, ' ', ' ', ' ', 'expired')
        else:

            return getResponse(404, ' ', ' ', ' ', 'FileError')
    else:

        return getResponse(404, ' ', ' ', ' ', 'urlError')


def getDynamoItem(path):
    dynamodbclient = boto3.resource('dynamodb')

    table = dynamodbclient.Table('fileuploadlookup')
    response = table.get_item(Key={'uri': path})

    if 'Item' in response:
        return response['Item']
    else:
        return False


def setItemMetadata(uri, key, value):
    dynamodbclient = boto3.resource('dynamodb')
    table = dynamodbclient.Table('fileuploadlookup')
    responce = table.update_item(
        Key={
            'uri': uri

        },
        UpdateExpression="SET metadata.#updated = :new_val",
        ExpressionAttributeNames={
            "#updated": key
        },
        ExpressionAttributeValues={
            ":new_val": value
        }
    )

    return responce


def getS3PreSignedURL(s3Bucket, objectKey):
    s3client = boto3.client(
        's3', 'eu-west-2', config=Config(signature_version='s3v4'))

    try:
        preSignedKey = s3client.generate_presigned_url('get_object',
                                                       Params={
                                                           'Bucket': s3Bucket, 'Key': objectKey},
                                                       ExpiresIn=86400)
        return preSignedKey
    except Exception as e:
        return False


def getResponse(statusCode, key, filename, filesize, status):
    body = {'key': key, 'filename': filename,
            'filesize': filesize, 'status': status}
    # return {'body': json.dumps(body)}
    return {
        'statusCode': statusCode,
        'headers': {"Access-Control-Allow-Origin": "*"},
        'body': json.dumps(body),
        'isBase64Encoded': False,
    }


####################################################################################################################################

# cleanup

####################################################################################################################################

@app.schedule('rate(1 hour)')
def cleanup(event):
    s3 = boto3.resource('s3')
    dynamodbclient = boto3.resource('dynamodb')
    table = dynamodbclient.Table('fileuploadlookup')

    # get all dynamo items where expiry < current timestamp or deleted == true
    response = table.scan(
        FilterExpression=Attr('metadata.expiry').lt(
            int(time.time())) | Attr('metadata.deleted').eq(True)
    )
    bucket = s3.Bucket(FILE_UPLOAD_BUCKET)
    for i in response['Items']:
        print("deleting item " + i['uri'])
        response = table.delete_item(
            Key={
                'uri': i['uri'],
            }
        )

        prefix = i['s3file'].split('/')
        s3Response = bucket.objects.filter(Prefix=prefix[0]).delete()

    return {
        'statusCode': 200,
        'body': json.dumps("")
    }
