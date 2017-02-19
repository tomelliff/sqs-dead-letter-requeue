#!/usr/bin/env python
from __future__ import print_function
import boto3
import os

def handler(event, context):
    messages_moved = requeue_all_messages()

    response = {
        "statusCode": 200,
        "body": "Total messages moved: {}".format(messages_moved)
    }

    return response

def _get_sqs_queues():
    active_queue_name = os.environ['QUEUE_NAME']
    dead_letter_queue_name = active_queue_name + "_dead_letter"

    sqs = boto3.resource('sqs')

    active_queue = sqs.get_queue_by_name(QueueName=active_queue_name)
    dead_letter_queue = sqs.get_queue_by_name(QueueName=dead_letter_queue_name)

    return (active_queue, dead_letter_queue)

def requeue_all_messages():
    active_queue, dead_letter_queue = _get_sqs_queues()

    total_messages_moved = 0

    while True:
        messages = dead_letter_queue.receive_messages(
                                            MaxNumberOfMessages=10,
                                            WaitTimeSeconds=20,
                                            VisibilityTimeout=20)
        number_of_messages = len(messages)
        if number_of_messages == 0:
            print('Requeuing messages done.')
            break
        else:
            print('Moving {} message(s)...'.format(number_of_messages))
            requeued_messages_to_send = []
            requeued_messages_to_delete = []
            for message in messages:
                requeued_messages_to_send.append({
                    'Id': message.message_id,
                    'MessageBody': message.body
                })
                requeued_messages_to_delete.append({
                    'Id': message.message_id,
                    'ReceiptHandle': message.receipt_handle
                })
            active_queue.send_messages(Entries=requeued_messages_to_send)
            dead_letter_queue.delete_messages(Entries=requeued_messages_to_delete)

        total_messages_moved += number_of_messages

    return total_messages_moved

if __name__ == '__main__':
    requeue_all_messages()
