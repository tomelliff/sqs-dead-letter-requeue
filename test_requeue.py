import os
import unittest

import boto3
from mock import patch
from moto import mock_sqs

import requeue

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
    os.environ['QUEUE_NAME']='queue_name'

    active_queue_name = os.environ['QUEUE_NAME']
    dead_letter_queue_name = active_queue_name + "_dead_letter"

    def setUp(self):
        sqs = boto3.resource('sqs')

        active_queue = sqs.create_queue(QueueName=self.active_queue_name)
        dead_letter_queue = sqs.create_queue(QueueName=self.dead_letter_queue_name)

    def test_get_sqs_queues_returns_active_and_dead_letter_queues(self):
        self.assertEqual(len(requeue._get_sqs_queues()), 2)
        self.assertTrue(requeue._get_sqs_queues()[0].url.endswith(self.active_queue_name))
        self.assertTrue(requeue._get_sqs_queues()[1].url.endswith(self.dead_letter_queue_name))


class TestRequeueAllMessages(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('requeue._get_sqs_queues')
        self.mock_get_sqs_queues = self.patcher.start()
        self.mock_get_sqs_queues.return_value = []

    class MockQueue(object):
        def __init__(self, queue_name):
            self.url = queue_name
            self.messages = []

        def put_messages_on_queue(number_of_messages):
            self.messages = [ 'message' ] * number_of_messages

        def receive_messages(self, **kwargs):
            return self.messages

    def provide_empty_queue(self, queue_name):
        mock_queue = self.MockQueue(queue_name)
        self.mock_get_sqs_queues.return_value.append(mock_queue)

    def provide_empty_queues(self):
        active_queue = self.provide_empty_queue('queue_name')
        dead_letter_queue = self.provide_empty_queue('queue_name_dead_letter')

        return (active_queue, dead_letter_queue)

    def put_messages_on_queue(self, number_of_messages, queue_name):
        self.mock_get_sqs_queues.return_value = 'foo'

    def test_empty_queue_returns_zero_messages_moved(self):
        self.provide_empty_queues()
        self.assertEqual(requeue.requeue_all_messages(),
                         0)


    def tearDown(self):
        self.patcher.stop()


if __name__ == '__main__':
    unittest.main()
