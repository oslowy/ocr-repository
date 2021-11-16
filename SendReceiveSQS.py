# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:13:50 2021

@author: AC
"""
import boto3
import json

class SQSQueue(object):
    def __init__(self,queueName=None):
        self.resource = boto3.client('sqs',region_name='us-east-1',
                                     aws_access_key_id='ASIA36UAVQEFXLYYKU52',
                                      aws_secret_access_key ='F+gIDe30HpS8c3cJBTm0W4t1cu0y7n6tuiKxZthN',
                                      aws_session_token='FwoGZXIvYXdzEND//////////wEaDIVkjK2rtJjNM6vNdyLAAXdFvvMnFrMj4NdilyOIIpvCUY7PCdPKOy21+nLN62pob2llIDOAnc4vWRVvRcrc6VyLEH25r5CRWCrjmKQTgKCgYZLtMxnzN9sqyALg1fg626EzF4Kpv7pbZvnS8VcKBYbnvlLqfO/HCKn/1HVojjbLZuSQxFp8hF6Y4jC3/dsEBoBSFR9Ea40z8AWdx1xj939I6IHWP+jmoiPGpF7xLC+S2xT1vVf8RysRxaFRk3Ke1aUE25DO2vErMHfXuNFXlyjv4smMBjIt5Nl9AIbxAOuk4TSCU6CmX+DXZQDtWbcdHcyMPWjtqTN2I7Cl/A46g8vGLj47')
         
        
    def receive(self):
        try:
            queue = self.resource.get_queue_by_name(QueueName='OCR')
            print(queue)
            msg=queue.receive_messages()
            for message in msg:
                data= message.body
                data= json.loads(data)
                message.delete()
                
        except Exception as e:
            print(e)
            return []
        return msg
    
    
    def send(self,QUEUE_URL, MSG_ATTRIBUTES, MSG_BODY):
        data=json.dumps(Message)
        response=self.resource.send_message(QueueUrl=QUEUE_URL,
                                            MessageAttributes=MSG_ATTRIBUTES
                                            ,MessageBody=MSG_BODY)
        return response
    
    
if __name__ == "__main__":
    
    QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/821682340107/OCR'
    MSG_ATTRIBUTES={
        'Title':{
            'DataType':'String',
            'StringValue':'Working with SQS in python using Boto3'}
        ,
        'Author':{
            'DataType':'String',
            'StringValue':'Working with SQS in python using Boto3'}
        }
    MSG_BODY = '00_01.jpg'

    q=SQSQueue(queueName='OCR')
    response = q.send(QUEUE_URL, MSG_ATTRIBUTES, MSG_BODY)
    # response = q.receive()
    json_msg = json.dumps(response,indent=4)
    print(json_msg)