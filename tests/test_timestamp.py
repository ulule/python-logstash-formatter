import datetime
import json
import logging
import unittest
from unittest import mock
import warnings

import logstash_formatter


class TimestampTest(unittest.TestCase):

    def setUp(self):
        self.record = logging.LogRecord(
            'test', logging.INFO, __file__, 1, 'message', (), None)

    def assertTimestamp(self, formatter, expected):
        now = datetime.datetime(
            2026, 10, 19, 12, 34, 56, 123456, tzinfo=datetime.timezone.utc)
        with mock.patch('logstash_formatter.datetime.datetime') as clock:
            clock.now.return_value = now
            clock.utcnow.side_effect = DeprecationWarning('utcnow is deprecated')
            output = json.loads(formatter.format(self.record))
            clock.now.assert_called_once_with(datetime.timezone.utc)
        self.assertEqual(output['@timestamp'], expected)

    def test_legacy_timestamp_preserves_microseconds(self):
        self.assertTimestamp(
            logstash_formatter.LogstashFormatter(),
            '2026-10-19T12:34:56.123456Z')

    def test_v1_timestamp_preserves_milliseconds(self):
        self.assertTimestamp(
            logstash_formatter.LogstashFormatterV1(),
            '2026-10-19T12:34:56.123Z')

    def test_formatting_does_not_emit_deprecation_warnings(self):
        with warnings.catch_warnings():
            warnings.simplefilter('error', DeprecationWarning)
            for formatter in (logstash_formatter.LogstashFormatter(),
                              logstash_formatter.LogstashFormatterV1()):
                output = json.loads(formatter.format(self.record))
                self.assertTrue(output['@timestamp'].endswith('Z'))
