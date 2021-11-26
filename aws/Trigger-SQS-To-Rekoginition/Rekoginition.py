
import json
import os
from datetime import datetime
from timeit import default_timer as timer
from Formats import dateTimeFormat
from datetime import datetime




def detect_text(rekognition,response):
    try:
        timeStart = timer()
        dateTimeStart = datetime.now().strftime(dateTimeFormat)
    
        print('Time for Detecting Text From Image started at ==> '+str(dateTimeStart))
            
        # print('image Recieved: =====>  '+str(response['Image']))
        
        responseFromRek = rekognition.detect_text(Image={'Bytes':response['Image']})
       
        timeEnd = timer()
        TextDetectionTime = timeEnd - timeStart
        print('Time for Detecting Text From Image completed at ==> '+str(TextDetectionTime))
     
        if responseFromRek is not None:
        
            textDetected=responseFromRek['TextDetections']
            finalResponse =[]
            for text in textDetected:
                textResponse={}
                textResponse = {'Detected text' : text['DetectedText'],
                'Confidence':"{:.2f}".format(text['Confidence']) + "%",
                'Id': '{}'.format(text['Id']),
                'Bounding Polygons':text['Geometry']['Polygon']
                }
                finalResponse.append(textResponse)
                
            response['StatusCode'] = 200
            response['TimeElapsed']['TimeEnd'] = TextDetectionTime
            response['FinalResponse'] = finalResponse
        
        else:
            response['StatusCode'] = 400
            
    except Exception as e:
        response['StatusCode'] = 500
        response['Error'] = str(e)
    

    return response


