"""Simple script to transmit event streams to AWS Kinesis.

Don't forget to set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
and STREAM_NAME
"""
import json
import os
import boto3
from sseclient import SSEClient as EventSource

STREAM_URL = 'https://stream.wikimedia.org/v2/stream/recentchange'
KINESIS_CLIENT = boto3.client('kinesis',
                              region_name='us-east-1',
                              aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                              aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
                              )
# So we don't flood our application we can set the limit of events to send
STREAM_COUNTER = 10


def main():
    """
    Main function to listen to event stream, parse and process to AWS Kinesis
    """
    counter = 0

    for event in EventSource(STREAM_URL):

        if counter > STREAM_COUNTER:
            break

        counter += 1

        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                data = ('{user} edited {title}'.format(**change))
                print(data)
                print('---')
                # Put the record into the stream
                KINESIS_CLIENT.put_record(StreamName=os.environ['STREAM_NAME'],
                                          Data=event.data,
                                          PartitionKey='partitionkey')

main()
