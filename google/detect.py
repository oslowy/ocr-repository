"""
Detects text and stores the result in the storage bucket.

Note: please configure the following Runtime Environment Variables:
BUCKET = name of the bucket containing the images and outputs
"""
import json
import os
from timeit import default_timer as timer


#################################################################################################
# Begin: Platform-independent. Reuse this code if possible.                                     #

def run_ocr(image, filename, approach, timings):                                                #
    time_start = timer()

    # Package the image in a request format for Google Vision
    request_image = {'content': image}

    # Detect the text
    annotations = text_detection(request_image)

    # Collect the output with timing information
    time_end = timer()

    timings['detect'] = time_end - time_start
    timings['total'] = time_end - timings['start']
    output_text = json.dumps({'annotations': annotations, 'timings': timings})

    # Store the output
    store_output(output_text, filename)

    return "Detected text and stored output."


# End: Platform-independent                                                                     #
#################################################################################################


#################################################################################################
# Begin: Google platform-specific. Younus: Re-implement using AWS client APIs.                  #

from google.cloud import vision, storage
from google.cloud.vision_v1 import EntityAnnotation


def format_response(text_detection_response):                                                    #
    """
    Converts the response from Vision into JSON.

    Younus: Extract all the DetectedText objects from Rekognition response and return them
            as a JSON list
    """

    #########################################################################################
    annotation_list = [json.loads(EntityAnnotation.to_json(a))  # Reimplement this line     #
                       for a in text_detection_response.text_annotations]                   #
    #########################################################################################

    return annotation_list


def text_detection(image):                                                                      #
    """
    Younus: Re-implement using Rekognition
    """
    #########################################################################################
    # Call Vision API                              # Reimplement this line                  #
    text_detection_response = vision.ImageAnnotatorClient().text_detection(image=image)  #
    #########################################################################################

    # Export as JSON string
    return format_response(text_detection_response)


def store_output(text, filename):                                                               #
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
