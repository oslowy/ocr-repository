"""
All the code in this file is designed to be platform-independent.
It should be reusable with AWS or Google.

    ### Younus: No need to change anything here.
"""
from timeit import default_timer as timer

import cv2
import numpy as np

from detect import detect


# Data loading
def cv_import(image):
    np_image = np.frombuffer(image, dtype=np.uint8)
    return cv2.imdecode(np_image, cv2.IMREAD_UNCHANGED)


def cv_export(processed_cv_image):
    return cv2.imencode('.png', processed_cv_image, [int(cv2.IMWRITE_PNG_BILEVEL), 1])[1].tobytes()


def load_params(approach):
    return approach.values()


# Processing script
def processing_operations(cv_image, approach):
    # Load parameters for image processing
    morph_kernel_size, \
    gauss_kernel_size, \
    thresh_window_size, \
    thresh_C = load_params(approach)

    # Convert to HSV
    hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    channels = cv2.split(hsv_image)

    # Noise removal and threshold
    for i in range(len(channels)):
        channels[i] = cv2.GaussianBlur(channels[i], (gauss_kernel_size, gauss_kernel_size), 0)
        channels[i] = cv2.adaptiveThreshold(channels[i], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                            thresh_window_size, thresh_C)
    # Combine channels
    thresholded_image = cv2.bitwise_or(channels[0], channels[1])

    # Morphological operations
    morphological_kernel = np.ones((morph_kernel_size, morph_kernel_size), np.uint8)
    opened_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_OPEN, morphological_kernel)
    closed_image = cv2.morphologyEx(opened_image, cv2.MORPH_CLOSE, morphological_kernel)

    return closed_image


def process(image, filename, approach, timings):
    time_start = timer()

    # Process the image
    cv_image = cv_import(image)
    processed_cv_image = processing_operations(cv_image, approach)
    processed_image = cv_export(processed_cv_image)

    # Record timing
    time_end = timer()
    timings['process'] = time_end - time_start

    return detect(processed_image, filename, approach, timings)
