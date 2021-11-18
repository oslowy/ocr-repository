"""
Legacy version of the load function that supports batch requests.

########################################################################################
### Younus: do not worry about re-implementing this, use the "load.py" file instead. ###
########################################################################################
"""

import threading
import os
from datetime import datetime
from timeit import default_timer as timer

from google.cloud import storage

from datetime_format import datetime_format
from detect import detect
from process import process


def select_publish_topic(is_processing_on):                                                     #
    return process if is_processing_on \
        else detect


def modify_filename(filename, date_time, is_processing_on):
    return f"{date_time}_{is_processing_on}/{filename[:-4]}"


def load_input(filename):
    bucket = os.getenv('BUCKET')

    return storage.Client().get_bucket(bucket) \
        .blob(f"img/{filename}") \
        .download_as_bytes()


def handle_image(filename, batch_start_time, is_processing_on, approach):
    # Load image from bucket
    time_start = timer()
    image = load_input(filename)

    # Modify filename by removing extension and adding time stamp and flags
    datetime_start = batch_start_time.strftime(datetime_format)
    filename = modify_filename(filename, datetime_start, is_processing_on)

    # Record timing for this function
    time_end = timer()
    timings = {'datetime_start': datetime_start,
               'load': time_end - time_start}

    # Pass to the next step
    return select_publish_topic(is_processing_on)(image, filename, approach, timings)


def start_batch(filenames, is_processing_on, approach):
    # Record current date and time to stamp output files
    batch_start_time = datetime.now()

    # Create threads to process batch
    threads = [threading.Thread(target=handle_image,
                                args=(filename, batch_start_time, is_processing_on, approach))
               for filename in filenames]

    # Start threads
    for thread in threads:
        thread.start()

    # Join threads
    for thread in threads:
        thread.join()

    # Complete
    return "All calls batched to image step. Outputs will be in " + \
           f"{batch_start_time.strftime(datetime_format)}_{is_processing_on}/"
