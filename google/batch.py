"""
Legacy version of the load function that supports batch requests.

########################################################################################
### Younus: do not worry about re-implementing this, use the "load.py" file instead. ###
########################################################################################
"""

import json
import threading
import os
from datetime import datetime

from google.cloud import storage, pubsub

from message import topic_res_name
from google.message import pack_message


def select_publish_topic(is_processing_on):
    topic_id = 'ocr-process-pickup' if is_processing_on \
        else 'ocr-detection-pickup'

    return topic_res_name(topic_id)


def modify_filename(filename, date_time, is_processing_on):
    return f"{date_time}_{is_processing_on}/{filename[:-4]}"


def load_input(filename):
    bucket = os.getenv('BUCKET')

    return storage.Client().get_bucket(bucket) \
        .blob(f"img/{filename}") \
        .download_as_bytes()


def handle_image(filename, batch_start_time, is_processing_on, approach):
    # Load image from bucket
    image = load_input(filename)

    # Modify filename by removing extension and adding time stamp and flags
    filename = modify_filename(filename, batch_start_time, is_processing_on)

    # Pack image and arguments into a message data object
    message_data = pack_message(image, filename, json.dumps(approach))

    pubsub.PublisherClient().publish(topic=select_publish_topic(is_processing_on),
                                     data=message_data)


def start_batch(filenames, is_processing_on, approach):
    # Record current date and time to stamp output files
    batch_start_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # e.g. 2021-11-30_11-30-00

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
    return "All calls batched to image step."
