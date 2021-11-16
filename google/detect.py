"""
Detects text and stores the result in the storage bucket.

Note: please configure the following Runtime Environment Variables:
BUCKET = name of the bucket containing the images and outputs
"""
import os
from functools import reduce


#################################################################################################
# Begin: Platform-independent. Reuse this code if possible.                                     #

def run_ocr(image, filename, approach):                                                         #
    # Package the image in a request format for Google Vision
    request_image = {'content': image}

    # Detect the text
    text = text_detection(request_image)

    # Store the output
    print(filename)
    store_output(text, filename)

    return "Detected text and published to next step."

# End: Platform-independent                                                                     #
#################################################################################################


#################################################################################################
# Begin: Google platform-specific. Younus: Re-implement using AWS client APIs.                  #

from google.cloud import vision, storage
from google.cloud.vision_v1 import EntityAnnotation


def format_response(text_detection_response):                                                   #
    """
    Converts the response from Vision into JSON.

    Younus: Extract all the DetectedText objects from Rekognition response and return them
            as a JSON list
    """

    #########################################################################################
    text_json_list = [EntityAnnotation.to_json(a)  # Reimplement this line                  #
                      for a in text_detection_response.text_annotations]                    #
    #########################################################################################

    if not text_json_list:
        return '[]'

    return '[\n' + reduce(lambda a, b: a + ',\n' + b, text_json_list) + '\n]'


def text_detection(image):                                                                      #
    """
    Younus: Re-implement using Rekognition
    """
    #########################################################################################
    # Call Vision API                              # Reimplement this line                  #
    text_detection_response = vision.ImageAnnotatorClient().text_detection(image=image)     #
    #########################################################################################

    # Export as JSON string
    return format_response(text_detection_response)


def store_output(text, filename):
    """
    Younus: Re-implement using S3
    """
    bucket = os.getenv('BUCKET')

    return storage.Client() \
        .get_bucket(bucket) \
        .blob(f"output/{filename}.txt") \
        .upload_from_string(text)

# End: Google platform-specific                                                                 #
#################################################################################################
