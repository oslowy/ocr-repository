import base64


def loadImage(s3Object, fileName,bucketName,key):


    print('Image Name from API ==> ',fileName)


    bucket = s3Object.Bucket(bucketName) 
    newKey = key=str(key)+str(fileName)
    obj = bucket.Object(newKey)      #pass your image Name to key

    response = obj.get()     #get Response
    print('Response from S3 ==> '+str(response))

    img = response[u'Body'].read()        # Read the respone, you can also print it.

    imageBase64 = base64.b64encode(img)          # Encoded the image to base64
    
    base_64_binary = base64.decodebytes(imageBase64)
    # return_json = str(imageBase64[0])           # Assing to return_json variable to return.  

    # print('return_json ========================>',return_json)


    return {
            'status': 'True',
           'statusCode': 200,
           'message': 'Downloaded profile image',
           'encoded_image':base_64_binary          # returning base64 of your image which in s3 bucket.
          } 