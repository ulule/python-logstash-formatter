'''
This library is provided to allow standard python
logging to output log data as JSON formatted strings
ready to be shipped out to logstash.
'''
import logging
import socket
import datetime
import traceback as tb
import json
import sys

def _default_json_default(obj):
    """
    Coerce everything to strings. 
    All objects representing time get output as ISO8601.
    """
    if isinstance(obj, datetime.datetime) or \
       isinstance(obj,datetime.date) or      \
       isinstance(obj,datetime.time):
        return obj.isoformat()
    else:
        return str(obj)

class LogstashFormatter(logging.Formatter):
    """
    A custom formatter to prepare logs to be
    shipped out to logstash.
    """

    def __init__(self,
                 source_host=None,
                 extra={},
                 json_cls=None,
                 json_default=_default_json_default):
        """
        :param source_host: override source host name
        :param extra: provide extra fields always present in logs
        :param json_cls: JSON encoder to forward to json.dumps
        :param json_default: Default JSON representation for unknown types,
                             by default coerce everything to a string
        """

        self.json_default = json_default
        self.json_cls = json_cls
        self.defaults = extra
        if source_host:
            self.source_host = source_host
        else:
            try:
                self.source_host = socket.gethostname()
            except:
                self.source_host = ""

    def format(self, record):
        """
        Format a log record to JSON, if the message is a dict
        assume an empty message and use the dict as additional
        fields.
        """

        fields = record.__dict__.copy()
        
        if isinstance(record.msg, dict):
            fields.update(record.msg)
            fields.pop('msg')
            msg = ""
        else:
            msg = record.getMessage()

        if 'msg' in fields:
            fields.pop('msg')

        if 'exc_info' in fields:
            if fields['exc_info']:
                formatted = tb.format_exception(*fields['exc_info'])
                fields['exception'] = formatted
            fields.pop('exc_info')

        if 'exc_text' in fields and not fields['exc_text']:
            fields.pop('exc_text')

        logr = self.defaults.copy()
        logr.update({'@message': msg,
                     '@timestamp': datetime.datetime.utcnow().isoformat(),
                     '@source_host': self.source_host,
                     '@fields': fields})

        return json.dumps(logr, default=self.json_default, cls=self.json_cls)
