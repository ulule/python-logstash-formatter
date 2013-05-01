import logging
import socket
import datetime
import traceback as tb
import json
import sys

class LogstashFormatter(logging.Formatter):
    def __init__(self, source_host=None, defaults={}):

        self.defaults = defaults
        if source_host:
            self.source_host = source_host
        else:
            try:
                self.source_host = socket.gethostname()
            except:
                self.source_host = ""

    def format(self, record):

        fields = record.__dict__
        
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
                     '@timestamp': datetime.datetime.now().isoformat(),
                     '@source_host': self.source_host,
                     '@fields': fields})

        print(logr)
        return json.dumps(logr)
