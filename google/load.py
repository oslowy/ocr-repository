"""
Loads an image file from the storage bucket.

Note: please configure the following Runtime Environment Variables:
BUCKET = name of the bucket containing the images
"""

#################################################################################################
# Begin: Platform-independent. Reuse this code if possible.                                     #
import os
from datetime import datetime
from timeit import default_timer as timer

from message import pack_message, publish
from datetime_format import datetime_format


def select_publish_topic(is_processing_on):                                                     #
    return 'ocr-process-pickup' if is_processing_on \
        else 'ocr-detection-pickup'


def modify_filename(filename, date_time, is_processing_on):                                     #
    return f"{date_time}_{is_processing_on}_{filename[:-4]}"


def load_and_publish(filename, is_processing_on, approach):                                     #
    # Record current date and time to stamp output files
    time_start = timer()
    datetime_start = datetime.now()  # e.g. 2021-11-30_11-30-00

    # Load image from bucket
    image = load_input(filename)

    # Modify filename by removing extension and adding time stamp and flags
    filename = modify_filename(filename, datetime_start, is_processing_on)

    # Record timing for this function
    time_end = timer()
    timings = {'datetime_start': datetime_start.strftime(datetime_format),
               'load': time_end - time_start}

    # Pack image and arguments into a message data object
    message_data = pack_message(image, filename, approach, timings)

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
