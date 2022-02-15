"""Simple event handler.

Listens to wiki recentchange events, gets the image list associated
and outputs a consolidated snapshot of article images after the edit
"""
import json
import platform_tools as pt


def lambda_handler(event, context):
    """Handler is called on event
    
    Args:
        event: Kinesis event of wiki recentchange
        context: Kineses context object
        
    Returns:
        List of record dicts ('recordId', 'result', 'data)
    """
    record_list = []
    
    # Stream is setup to process records in bulk but would also work on single events
    for record in event['records']:

       # Event is encoded, so we decode here
       payload=pt.format_input(record["data"])
 
       # Get the page title so we can call MW API
       page_title = json.loads(payload)['title']
       
       # Get the list of images from MW API
       image_list = pt.call_api(page_title)
       
       # Format the list into our schema
       page_id,formatted_image_list = pt.format_image_list(image_list)
       
       record_list.append(pt.format_output_dict(record['recordId'],
                                                formatted_image_list,
                                                page_id))
    
    # Return a list of records
    return pt.format_output_list(record_list)
