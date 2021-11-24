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

from datetime_format import datetime_format
from detect import detect
from process import process


def select_next_phase(is_processing_on):                                                     #
    return process if is_processing_on \
        else detect


def modify_filename(filename, date_time, is_processing_on):                                     #
    return f"{date_time}_{is_processing_on}_{filename[:-4]}"


def load(filename, is_processing_on, approach):                                                 #
    # Record current date and time to stamp output files
    time_start = timer()
    datetime_start = datetime.now().strftime(datetime_format)

    # Load image from bucket
    image = load_input(filename)

    # Modify filename by removing extension and adding time stamp and flags
    filename = modify_filename(filename, datetime_start, is_processing_on)

    # Record timing for this function
    time_end = timer()
    timings = {'datetime_start': datetime_start,
               'load': time_end - time_start}

    # Pass to the next step
    return select_next_phase(is_processing_on)(image, filename, approach, timings)

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
