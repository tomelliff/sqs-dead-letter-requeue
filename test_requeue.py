import unittest

from mock import Mock

import requeue

class TestHandler(unittest.TestCase):
    def setUp(self):
        requeue.requeue_all_messages = Mock(return_value=3)

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


if __name__ == '__main__':
    unittest.main()
