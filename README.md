# Simple Streams POC

The purpose of this repo is to demonstrate how simple it is to write an application in Python that consumes an event, transforms it and outputs it somewhere else.

To run this process you will need an AWS Kinesis stream to write to.

The process can be run as follows:

1. Simple Python script that listens to an existing event stream over HTTP and send to AWS Kinesis stream.

```
pip install boto3
pip install sseclient

export AWS_ACCESS_KEY_ID=???
export AWS_SECRET_ACCESS_KEY=???
export STREAM_NAME=???

python stream_processor.py
```
