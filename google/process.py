"""
All the code in this file is designed to be platform-independent.
It should be reusable with AWS or Google.

    ### Younus: No need to change anything here.
"""
import json

import cv2
import numpy as np

from message import publish, pack_message


# Data loading
def cv_import(image):
    np_image = np.frombuffer(image, dtype=np.uint8)
    return cv2.imdecode(np_image, cv2.IMREAD_UNCHANGED)


def cv_export(processed_cv_image):
    return cv2.imencode('.png', processed_cv_image, [int(cv2.IMWRITE_PNG_BILEVEL), 1])[1]


def load_params(approach):
    return json.loads(approach).values()


# Thresholding
def rgb_thresholding(cv_image, gauss_kernel_size, thresh_window_size, thresh_C):
    channels = cv2.split(cv_image)
    channels = [cv2.GaussianBlur(channel, (gauss_kernel_size, gauss_kernel_size), 0)
                for channel in channels]
    channels = [cv2.adaptiveThreshold(channel, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                      thresh_window_size, thresh_C)
                for channel in channels]

    return cv2.cvtColor(cv2.merge(channels), cv2.COLOR_RGB2GRAY)


def gray_thresholding(cv_image, gauss_kernel_size, thresh_window_size, thresh_C):
    grayed_img = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
    blurred_img = cv2.GaussianBlur(grayed_img, (gauss_kernel_size, gauss_kernel_size), 0)
    return cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY_INV, thresh_window_size, thresh_C)


# Morphological operations
def morphological(image, morph_kernel_size):
    morphological_kernel = np.ones((morph_kernel_size, morph_kernel_size), np.uint8)
    opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, morphological_kernel)
    return cv2.morphologyEx(opened_image, cv2.MORPH_CLOSE, morphological_kernel)


# Processing script
def process_image(cv_image, approach):
    # Load parameters for image processing
    morph_kernel_size, \
    gauss_kernel_size, \
    thresh_window_size, \
    thresh_C, \
    rgb_threshold, \
    debug = load_params(approach)

    # Thresholding
    thresholded_image = (rgb_thresholding if rgb_threshold else gray_thresholding)\
        (cv_image, gauss_kernel_size, thresh_window_size, thresh_C)

    # Morphological operations
    morphed_image = morphological(thresholded_image, morph_kernel_size)

    return morphed_image


def process_publish(image, filename, approach):
    # Process the image
    cv_image = cv_import(image)
    processed_cv_image = process_image(cv_image, approach)
    processed_image = cv_export(processed_cv_image)

    # Re-package the image and arguments and publish
    message = pack_message(processed_image, filename, approach)
    publish('ocr-detection-pickup', message)

    return "Ran processing and published to next step."
