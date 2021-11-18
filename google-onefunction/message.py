"""
Helper functions for receiving HTTP request.
The file contains Google-specific code.
"""

#################################################################################################
# Begin: Google platform-specific. Younus: Re-implement using AWS client APIs.                  #


def extract_args_http(request):                                                                 #
    """
    Google platform-specific.

    Younus: re-implement using
        data = json.loads(request.body)['data']

        in place of

        request.get_json(silent=True)['data']
    """
    #######################################################################
    data = request.get_json(silent=True)['data']  # Reimplement this line #
    #######################################################################

    approach = data['approach'] if ('approach' in data) and data['is_processing_on'] else {}

    filename_arg = data['filenames'] if 'filenames' in data else data['filename']

    return filename_arg, data['is_processing_on'], approach

# End: Google platform-specific                                                                 #
#################################################################################################
