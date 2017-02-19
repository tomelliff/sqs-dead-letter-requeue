import os
import unittest

import boto3
from mock import patch
from moto import mock_sqs

import requeue

os.environ['QUEUE_NAME']='queue_name'

active_queue_name = os.environ['QUEUE_NAME']
dead_letter_queue_name = active_queue_name + "_dead_letter"

class TestHandler(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('requeue.requeue_all_messages')
        self.mock_requeue_all_messages = self.patcher.start()
        self.mock_requeue_all_messages.return_value = 3

    def test_handler_calls_main_logic(self):
        requeue.handler('event', 'context')
        requeue.requeue_all_messages.assert_called_once_with()

    def test_handler_returns_dict_response(self):
        self.assertEqual(type(requeue.handler('event', 'context')),
                         type({}))

    def test_handler_returns_200_status_code(self):
        self.assertEqual(requeue.handler('event', 'context')['statusCode'],
                         200)

    def test_handler_returns_body_with_total_messages_processed(self):
        self.assertEqual(requeue.handler('event', 'context')['body'],
                         'Total messages moved: 3')

    def tearDown(self):
        self.patcher.stop()

@mock_sqs
class TestGetSqsQueues(unittest.TestCase):
    def setUp(self):
        sqs = boto3.resource('sqs')

        active_queue = sqs.create_queue(QueueName=active_queue_name)
        dead_letter_queue = sqs.create_queue(QueueName=dead_letter_queue_name)

    def test_get_sqs_queues_returns_active_and_dead_letter_queues(self):
        self.assertEqual(len(requeue._get_sqs_queues()), 2)
        self.assertTrue(requeue._get_sqs_queues()[0].url.endswith(active_queue_name))
        self.assertTrue(requeue._get_sqs_queues()[1].url.endswith(dead_letter_queue_name))

@mock_sqs
class TestRequeueAllMessages(unittest.TestCase):
    def put_messages_on_queue(self, queue_name, number_of_messages):
        messages = [{
            'Id': '1',
            'MessageBody': 'message body'
        }] * number_of_messages
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=queue_name)
        queue.send_messages(Entries=messages)

    def test_empty_queue_returns_zero_messages_moved(self):
        self.assertEqual(requeue.requeue_all_messages(poll_wait=0),
                         0)

    def test_non_empty_queue_returns_correct_messages_moved(self):
        number_of_messages = 10
        self.put_messages_on_queue(dead_letter_queue_name, number_of_messages)
        self.assertEqual(requeue.requeue_all_messages(poll_wait=0),
                         number_of_messages)

if __name__ == '__main__':
    unittest.main()
