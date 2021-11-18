"""
Helper functions for sending and receiving messages between Lambda functions.
The first part of the file contains cross-platform code. The second part
contains Google-specific code.
"""

#############################################################################
# Begin: Platform-independent. Reuse this code if possible.                 #
import base64
import json
import os


def pack_message(image, filename, approach, timings):                       #
    # Convert the image to a string in base64 format
    content_str = base64.b64encode(image).decode('ascii')

    return pack_text_message(content_str, filename, approach, timings)


def unpack_message(event):                                                  #
    content_str, filename, approach, timings = unpack_text_message(event)

    # Get the image from the coded string
    image = base64.b64decode(content_str.encode('ascii'))

    return image, filename, approach, timings


def pack_text_message(text, filename, approach, timings):                   #
    message = {'content': text,
               'filename': filename,
               'approach': approach,
               'timings': timings}

    # Convert the complete package into a binary object containing JSON
    return json.dumps(message).encode('utf-8')
# End: Platform-independent                                                 #
#############################################################################


#################################################################################################
# Begin: Google platform-specific. Younus: Re-implement using AWS client APIs.                  #
from google.cloud import pubsub


def unpack_text_message(event):
    """
    Partially Google platform-specific.

    Younus: the base64 decoding is not needed in this part. Also, AWS uses a different attribute
            structure for message events. If you set up your lambdas to trigger from an SQS,
            you will NOT need to call receive() from boto3, just send() them from the preceding
            lambda and set up this method here to unpack the data from the event structure.

            I think the access structure you want is:
            message_data = event['Records'][0]['body']

            after that everything else should be fine.
    """
    # Unpack the binary JSON object
    ####################################################################################################
    message_data = base64.b64decode(event["data"])      # message_data = event['Records'][0]['body']   #
    ####################################################################################################
    message = json.loads(message_data.decode("utf-8"))

    return message['content'], message['filename'], message['approach'], \
           message['timings']


def extract_args_http(request):                                                                 #
    """
    Google platform-specific.

    Younus: re-implement using
        data = json.loads(message.body)['data']

        in place of

        request.get_json(silent=True)['data']
    """
    #######################################################################
    data = request.get_json(silent=True)['data']  # Reimplement this line #
    #######################################################################

    approach = data['approach'] if ('approach' in data) and data['is_processing_on'] else {}

    filename_arg = data['filenames'] if 'filenames' in data else data['filename']

    return filename_arg, data['is_processing_on'], approach


def topic_res_name(topic_id):                                                                   #
    """
    Google platform-specific.

    Younus: Reimplement using SQS_client.get_queue_by_name(topic_id) as seen in existing
    SendReceiveSQS code

    ### Note: there is no need to use Access Keys, Session Tokens, etc. for boto3 when
        you are calling the SQS or other resources from within the lambda.
    """

    #########################################################################
    project = os.getenv('PROJECT')  # Remove these lines and redo           #

    return f"projects/{project}/topics/{topic_id}"                          #
    #########################################################################


def publish(topic, message):                                                                    #
    """
    Google platform-specific.

    Younus: Reimplement using SQS client
    """

    ############################################################################################
    pubsub.PublisherClient().publish(topic=topic_res_name(topic),  # Remove these lines & redo #
                                     data=message)                                             #
    ############################################################################################

# End: Google platform-specific                                                                 #
#################################################################################################
