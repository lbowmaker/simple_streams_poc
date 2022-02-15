import json
import base64
from botocore.vendored import requests
import datetime

# API URL to get image list
# TO DO: Make this non en specific
IMAGE_URL = 'http://en.wikipedia.org/w/api.php?action=query&prop=images&titles={}&format=json&imlimit=500'


def format_input(event):
    """Decode a Kineses event.

    Args:
        event: Kinesis event (encoded)

    Returns:
        Kinesis event (decoded)
    """
    return base64.b64decode(event)


def format_output_list(output_list):
    """Format a list to AWS expected output

    Args:
        output_list: list

    Returns:
        dict: containing list of records
    """
    return {
        "records": output_list
    }


def format_output_dict(record_id, output, page_id):
    """Format a dict to AWS expected output

    Args:
        record_id(str): AWS input record id
        output (dict): Formatted output
        page_id (str): Wiki page id

    Returns:
        dict: required format for AWS to process
    """
    return {
        "recordId": record_id,
        "result": "Ok",
        "data": create_output_format(page_id, output)
    }


def call_api(page_title):
    """Calls MW API using requests

    Args:
        page_title(str): Wiki page title

    Returns:
        json: response from MW API
    """
    return requests.get(IMAGE_URL.format(page_title)).json()


def format_image_list(image_json):
    """Format image list from MW API call

    Args:
        image_json (json): MW API response

    Returns:
        str: page_id
        list: of images
    """
    page_id = '-1'

    try:
        keys = list(image_json['query']['pages'].keys())
        
        page_id = keys[0]

        image_list = image_json['query']['pages'][page_id]['images']

        formatted_image_list = []

        for image in image_list:
            formatted_image_list.append((image['title']))

        return page_id, formatted_image_list
    except KeyError:
        return page_id, []


def create_output_format(page_id, image_list):
    """Format data to the new schema

    Args:
        page_id(str): Wiki page id
        image_list: list of image names

    Returns:
        dict: schema for new output
    """
    return {
        'page_id': page_id,
        'image_list': image_list,
        'create_date_time': datetime.datetime.now().isoformat()
    }
