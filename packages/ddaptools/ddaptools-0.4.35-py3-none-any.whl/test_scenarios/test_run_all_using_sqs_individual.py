import boto3
from ddaptools.aws_classes.class_enhancement import *
from ddaptools.dda_constants import *
import uuid

sqs = boto3.client('sqs')

# Define the URL of your SQS queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/796522278827/ProcessingQueue.fifo'

def test_enqueue_all():
    
    
    message_deduplication_id = str(uuid.uuid4())

    for staging_guid in [
        'd3927aff-a03d-439d-b729-64236004443b',
        'e5e4b6f2-032e-4e33-a588-f429fe7f7a2f',
        '014bb5b2-60ed-494e-a5d0-507efb63592e',
        ]:
        print("Enqueue: ", staging_guid)
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=staging_guid,
            MessageGroupId=staging_guid,
            MessageDeduplicationId=message_deduplication_id,
        )
        print(response)


