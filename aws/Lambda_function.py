from __future__ import print_function
import boto3
from decimal import Decimal
import json
import urllib.request
import urllib.parse
import urllib.error

print('Loading function')

    
rekognition = boto3.client('rekognition')
sqs = boto3.client('sqs',region_name='us-east-1',
                                      # QueueUrl='https://sqs.us-east-1.amazonaws.com/821682340107/OCR',
                                      aws_access_key_id='ASIA36UAVQEFXLYYKU52',
                                      aws_secret_access_key ='F+gIDe30HpS8c3cJBTm0W4t1cu0y7n6tuiKxZthN',
                                      aws_session_token='FwoGZXIvYXdzEND//////////wEaDIVkjK2rtJjNM6vNdyLAAXdFvvMnFrMj4NdilyOIIpvCUY7PCdPKOy21+nLN62pob2llIDOAnc4vWRVvRcrc6VyLEH25r5CRWCrjmKQTgKCgYZLtMxnzN9sqyALg1fg626EzF4Kpv7pbZvnS8VcKBYbnvlLqfO/HCKn/1HVojjbLZuSQxFp8hF6Y4jC3/dsEBoBSFR9Ea40z8AWdx1xj939I6IHWP+jmoiPGpF7xLC+S2xT1vVf8RysRxaFRk3Ke1aUE25DO2vErMHfXuNFXlyjv4smMBjIt5Nl9AIbxAOuk4TSCU6CmX+DXZQDtWbcdHcyMPWjtqTN2I7Cl/A46g8vGLj47')
s3 = boto3.client('s3')
# --------------- Helper Functions to call Rekognition APIs ------------------

def receive(event):
    try:
        records = event["Records"]
        for record in records:
            payload = record["body"]
            data= json.loads(json.dumps(payload,default=str))
    except Exception as e:
        return [[],e]
    return [data,None]
    
    
def GetFileFromS3(bucket,key):
    try:
        s3Object = s3.get_object(Bucket=bucket, Key=key)
        image = s3Object['Body'].read()
        return image
    except Exception as e:
        print(e)
        raise e

def detect_faces(bucket, key):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response


def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    # Sample code to write response to DynamoDB table 'MyTable' with 'PK' as Primary Key.
    # Note: role used for executing this Lambda function should have write access to the table.
    #table = boto3.resource('dynamodb').Table('MyTable')
    #labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    #table.put_item(Item={'PK': key, 'Labels': labels})
    return response

def detect_text(bucket, key):
    response = rekognition.detect_text(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    count = len(response['TextDetections'])
    textDetections=response['TextDetections']
    finalResponse =[]
    for text in textDetections:
        textResponse={}
        textResponse = {'Detected text' : text['DetectedText'],
        'Confidence':"{:.2f}".format(text['Confidence']) + "%",
        'Id': '{}'.format(text['Id'])
        }
        # if 'ParentId' in text:
        #     parentType = {
        #         'Parent Id': '{}'.format(text['ParentId']),
        #         'Type' :text['Type']
        #     }
        #     json.dump(parentType,textResponse)
        finalResponse.append(textResponse)
    return finalResponse

def index_faces(bucket, key):
    # Note: Collection has to be created upfront. Use CreateCollection API to create a collecion.
    #rekognition.create_collection(CollectionId='BLUEPRINT_COLLECTION')
    response = rekognition.index_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}}, CollectionId="BLUEPRINT_COLLECTION")
    return response


# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    
    try:
        # Calls rekognition DetectFaces API to detect faces in S3 object
        # response = detect_faces(bucket, key)
        response = receive(event)
        
            # record.delete()
        # Calls rekognition DetectLabels API to detect labels in S3 object
        #response = detect_labels(bucket, key)

        # Calls rekognition IndexFaces API to detect faces in S3 object and index faces into specified collection
        #response = index_faces(bucket, key)

        # Print response to console.
        # print(response)
        # records.delete()
        # print(response[1])
        # if response[1] is not None :
        if True:
            # Get the object from the event
            bucket = 'ocr-image-data-sqs'
            key = 'Google-Street-View-Data/'
            fileName=response[0]
            # image = GetFileFromS3(bucket,key+fileName) 
            image = detect_text(bucket,key+fileName) 
            if image is not None:
                print(response[0])
                print(image)
                return image
                # return json.dumps( response[0])

        else:
            return response[0]
 
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
