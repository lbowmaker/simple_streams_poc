# Simple Streams POC

**NOTE**: This POC does not aim to recommend AWS as a solution but is an evaluation of features and a simple way to implement a streaming application.

To run this process you will need an AWS Kinesis stream to write to.

The process can be run as follows:

**1. Create a data stream in AWS Kinesis**

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

https://github.com/lbowmaker/simple_streams_poc/blob/ae21d3eca23e9e30f285e6b9778dafd72f2de2ca/wiki_image_list/lambda_function.py#L1-L42

**5. Create a Data Delivery Stream**

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
- Streams web UI provides a nice interface to the streams, the API and actual data - Kinesis didn't really do this without digging around in logs/execution pages

### Pros

- Reduces thoughts about compute power to a minimum
- Allows easy backfilling of streams from timestamp or message id
- Took less than a day to cobble something together
- Can deploy AWS Lambda functions as HTTP endpoints so they could be used elsewhere (not just events)

## Things we might want to copy...

- Easy self service of input event stream > execute process > output somewhere (file store, database, other stream)
- Allow services to start up against timestamp from stream (not every service will need all of the data back to day 1)
- Endpoints aren't tied to just event stream execution, can be called independently like an API
