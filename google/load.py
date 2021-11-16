"""
Loads an image file from the storage bucket.

Note: please configure the following Runtime Environment Variables:
BUCKET = name of the bucket containing the images
"""

#################################################################################################
# Begin: Platform-independent. Reuse this code if possible.                                     #
import json
import os
from datetime import datetime

from google.message import pack_message
from message import publish


def select_publish_topic(is_processing_on):                                                     #
    return 'ocr-process-pickup' if is_processing_on \
        else 'ocr-detection-pickup'


def modify_filename(filename, date_time, is_processing_on):                                     #
    return f"{date_time}_{is_processing_on}_{filename[:-4]}"


def load_and_publish(filename, is_processing_on, approach):                                     #
    # Record current date and time to stamp output files
    start_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # e.g. 2021-11-30_11-30-00

    # Load image from bucket
    image = load_input(filename)

    # Modify filename by removing extension and adding time stamp and flags
    filename = modify_filename(filename, start_time, is_processing_on)

    # Pack image and arguments into a message data object
    message_data = pack_message(image, filename, json.dumps(approach))

    # Publish to the queue
    publish(topic=select_publish_topic(is_processing_on),
            message=message_data)

    # Complete
    return f"Loaded {filename} and published to next step."

# End: Platform-independent                                                                     #
#################################################################################################

#################################################################################################
# Begin: Google platform-specific. Younus: Re-implement using AWS client APIs.                  #
from google.cloud import storage


def load_input(filename):
    bucket = os.getenv('BUCKET')

    return storage.Client().get_bucket(bucket) \
        .blob(f"img/{filename}") \
        .download_as_bytes()

# End: Google platform-specific                                                                 #
#################################################################################################
