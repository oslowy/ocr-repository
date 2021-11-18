"""
The code in this file may or may not be needed for AWS. It was included
to support Google's way of configuring Cloud Functions. If your Lambda
functions support custom entry point filenames, you may not need this
but it will not hurt anything either necessarily.
"""
import load
import detect
import message as msg
import process


def load_entry(request):
    return load.load(
        *msg.extract_args_http(request))


#####################################################################
# Legacy code to support batch loading.                             #
#                                                                   #
# Younus: delete for AWS version                                    #
import batch


def batch_entry(request):                                           #
    return batch.start_batch(
        *msg.extract_args_http(request))
#####################################################################
