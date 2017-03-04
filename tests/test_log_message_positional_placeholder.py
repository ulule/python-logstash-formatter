import logging
from six import StringIO
import unittest

import logstash_formatter


class LogMessagePositionalPlaceholderTest(unittest.TestCase):

    def setUp(self):
        self.stream = StringIO()
        handler = logging.StreamHandler(self.stream)
        handler.setFormatter(logstash_formatter.LogstashFormatterV1())
        handler.setLevel(logging.DEBUG)
        self.log = logging.getLogger('test')
        self.log.addHandler(handler)
        self.log.setLevel(logging.DEBUG)

    def assertLogMessage(self, msg):
        self.assertTrue(
            '"message": "{}"'.format(msg) in self.stream.getvalue())


test_msgs = {
    'normal_log_message': 'foo',
    'implicit_positional_placeholder': '{}',
    'explicit_positional_placeholder': '{0}',
    'message_with_invalid_formatting': '{'
}


def make_method(msg):

    def test_msg(self):
        self.log.debug(msg)
        self.assertLogMessage(msg)

    return test_msg


for name, msg in test_msgs.items():
    name = 'test_{}'.format(name)
    setattr(LogMessagePositionalPlaceholderTest, name, make_method(msg))
