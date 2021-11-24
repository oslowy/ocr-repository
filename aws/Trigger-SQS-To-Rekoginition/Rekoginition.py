


# --------------- Helper Functions to call Rekognition APIs ------------------


def detect_text(rekognition,image):
    print('image Recieved: =====>  '+str(image))
    response = rekognition.detect_text(Image={'Bytes':image})
    count = len(response['TextDetections'])
    textDetections=response['TextDetections']
    finalResponse =[]
    for text in textDetections:
        textResponse={}
        textResponse = {'Detected text' : text['DetectedText'],
        'Confidence':"{:.2f}".format(text['Confidence']) + "%",
        'Id': '{}'.format(text['Id']),
        'Bounding Polygons':text['Geometry']['Polygon']
        }
        finalResponse.append(textResponse)
    return finalResponse


