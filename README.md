# Simple Streams POC

**NOTE**: This POC does not aim to recommend AWS as a solution but is an evaluation of features and a simple way to implement a streaming application.

To run this process you will need an AWS Kinesis stream to write to.

The process can be run as follows:

**1. Create a data stream in AWS Kinesis:**

![Kinesis_Data_Stream](https://user-images.githubusercontent.com/93719848/154076403-effbaac4-95a9-47e9-b71d-bedf68e605e1.png)

**2. Send event messages to Kinesis data stream**

Simple Python script that listens to an existing event stream over HTTP and sends to AWS Kinesis stream.

```
pip install boto3
pip install sseclient

export AWS_ACCESS_KEY_ID=???
export AWS_SECRET_ACCESS_KEY=???
export STREAM_NAME=???

python stream_processor.py
```

**3. AWS Lambda**

AWS Lambda function that listens to the stream, gets associated article images and outputs the data

```python
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
```

**5. Create a Data Delivery Stream

An AWS delivery stream calls the AWS Lamba function (wiki_image_list - see code above) on event trigger and writes the output to an S3 bucket (for ease).

![ Kinesis_Delivery_Stream](https://user-images.githubusercontent.com/93719848/154101477-98de0110-bd5f-411f-9fcb-fc8a526bb6c1.png)

**6. Review output schema:**

Our process outputs data in this format:

```json
{
	"page_id": "25577439",
	"image_list": [
		"File:Commons-logo.svg",
		"File:Flag of Brazil.svg",
		"File:P vip.svg"
	],
	"create_date_time": "2022-02-15T15:37:52.151917"
}
```

**7. Consumers**

Can subscribe to the stream or query key/value store to see state of images at a given time


## Conclusions

### Cons

- Seemed too easy to create streams that didn't have a schema associated to them
- Couldn't use Python requests in AWS Lambda, had to use Py3.6 and botocore.vendored import requests. Seems like you would have to manage Python changes on top of Amazon implementation of it which could be challenging (I suspect there are other instances of this too).
- Python error messages less verbose in AWS Lambda
- AWS Lambda UI is nice for less experienced developers to create something quickly but it's not industry standard and abstracts somethings that might be useful to learn (writing tests, commiting to repo's, etc)
- Even though lots of technical things are abstracted you would need someone to manage roles and access which gets quite complicated/involved easily
- Didn't seem that the code editor UI would make for good collaboration unless you managed code externally

### Pros

- Reduces thoughts about compute power to a minimum
- Allows easy backfilling of streams from timestamp or message id
- Took less than a day to cobble something together
- Can deploy AWS Lambda functions as HTTP endpoints so they could be used elsewhere (not just events)
