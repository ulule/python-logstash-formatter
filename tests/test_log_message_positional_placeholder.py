import logging
import StringIO
import unittest

import logstash_formatter


class LogMessagePositionalPlaceholderTest(unittest.TestCase):

    def setUp(self):
        self.stream = StringIO.StringIO()
        handler = logging.StreamHandler(self.stream)
        handler.setFormatter(logstash_formatter.LogstashFormatter())
        handler.setLevel(logging.DEBUG)
        self.log = logging.getLogger('test')
        self.log.addHandler(handler)
        self.log.setLevel(logging.DEBUG)

    def assertLogMessage(self, msg):
        self.assertTrue(
            '"@message": "{}"'.format(msg) in self.stream.getvalue())


test_msgs = {
    'normal_log_message': 'foo',
    'implicit_positional_placeholder': '{}',
    'explicit_positional_placeholder': '{0}',
    'unbalanced_curly_brace': '{'
}


def make_method(msg):

    def test_msg(self):
        self.log.debug(msg)
        self.assertLogMessage(msg)

    return test_msg


for name, msg in test_msgs.items():
    setattr(LogMessagePositionalPlaceholderTest, name, make_method(msg))
