#!/usr/bin/env python
# Taken from https://github.com/boto/boto3/issues/324#issuecomment-151563366
import boto3
import sys

"""Bulk loads test messages on to a given queue.

Pass queue name when calling script.
eg. python seed_queue.py test_queue
"""

sqs_queue_name = sys.argv[1]

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=sqs_queue_name)

for i in range(10):
    messages = []
    for j in range(10):
        n = str(i * 10 + j)
        messages.append({
            "Id": n,
            "MessageBody": "Message %s" % n
        })
    queue.send_messages(Entries=messages)
