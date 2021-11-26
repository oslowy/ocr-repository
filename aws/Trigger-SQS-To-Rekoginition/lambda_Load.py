import boto3
from decimal import Decimal
import json
import urllib.request
import urllib.parse
import urllib.error
from lambda_Load import loadImage
from Rekoginition import detect_text
from PreProcessing import process
from Formats import dateTimeFormat
from datetime import datetime
# import eval

print('Loading function')

rekognition = boto3.client('rekognition')
s3 = boto3.resource("s3")




def SaveFileToS3(bucket,writekey,response):
    
   
    s3Object = s3.Object(bucket,writekey+response['NewFileName']+".json")
    # print(type(response['FinalResponse']))
    resp = {'Text Detected': response['FinalResponse']}
    resp = json.dumps(resp).encode("UTF-8")
    # resp = resp.replace("b'","")  
    s3Object.put(
      Body =  (bytes(resp)),
      ContentType='application/json'
        )
    # encoded_Json = imageData.encode=("utf-8")
    # s3.Bucket(bucket).put_object(key=key,Body= encoded_Json)
    response['StatusCode'] = 200

    return response
    
 
def lambda_handler(event, context):
    isProcessingOn=False 
    approach={
        "morph_kernel_size": 5,
		"gauss_kernel_size": 7,
		"thresh_window_size": 2,
		"thresh_C": 5
    }
     
    bucket = 'ocr-image-dataset'
    key = 'Google-Street-View-Data/'
    writekey = 'Google-Street-View-Data-Result-Text/'
    try:

        body = event['Records'][0]["body"]
        print(type(body))
        
        body = json.loads(body) 

        fileName = body['data']['filename']
        isProcessingOn=body['data']['is_processing_on'] 
        approach= body['data']['approach']
        print(fileName)
        print(isProcessingOn)
        print(approach)
        response = loadImage(s3, fileName, bucket, key, isProcessingOn)
        
        if response['StatusCode'] != 200:
            
            return {'StatusCode':response['StatusCode'],
                            'Message':'Image not found on Location: '+bucket+'/'+key+'/'+fileName,
                            'Error': response['Error']
                            }
        else:
           
            print(type(response['Image']))
            
            if isProcessingOn == True:
                
                print("Processing Feature is ON")
                
                response = process(response, approach)
                
                print("Response Received From Preprocessing.")
                
                if response['StatusCode'] != 200:
                    return {'StatusCode':response['StatusCode'],
                            'Message':'Pre processing failed error occured',
                            'Error': response['Error']
                            }
                    
            print('Going For Text Detection')
            
            response = detect_text(rekognition,response) 

            print('Response Received from Text Detection')
                
            if response['StatusCode'] != 200:
                return {'StatusCode':response['StatusCode'],
                            'Message':'Text Detection Failed error occured',
                            'Error': response['Error']
                            }
            # fileNameWithoutExt = fileName.split('.')[0]
            
            response = SaveFileToS3(bucket,writekey,response)
            print('Response saved to S3')

            if response['StatusCode'] != 200:
                return {'StatusCode':response['StatusCode'],
                            'Message':'Failed To Save the file back to S3 bucket',
                            'Error': response['Error']
                            }
                            
            else:
                
                return response['FinalResponse']

       
    except Exception as e:
        return {'StatusCode':500,
                'Message':'Error processing object {} from bucket {}. '.format(key, bucket) +
              'Make sure your object and bucket exist and your bucket is in the same region as this function.',
                'Error': str(e)
                }
  
