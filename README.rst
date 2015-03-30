logstash_formatter: JSON logs for logstash
==========================================

This library is provided to allow standard python logging to output log data
as json objects ready to be shipped out to logstash.

Installing
----------
Pip:

    ``pip install logstash_formatter``

Pypi:

   https://pypi.python.org/pypi/logstash_formatter

Manual:

    ``python setup.py install``

Usage
-----

Json outputs are provided by the LogstashFormatter logging formatter.

::

    import logging
    from logstash_formatter import LogstashFormatter

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = LogstashFormatter()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

The LogstashFormatter may take the following named parameters:

* ``fmt``: Config as a JSON string that supports:
  * ``extra``: provide extra fields always present in logs
  * ``source_host``: override source host name
* ``json_cls``: JSON encoder to forward to ``json.dump``
* ``json_default``: Default JSON representation for unknown types,
    by default coerce everything to a string

You can also add extra fields to your json output by specifying a dict in place of message, or by specifying
the named argument ``extra`` as a dictionary. When supplying the ``exc_info`` named argument with a truthy value,
and if an exception is found on the stack, its traceback will be attached to the payload as well.

::

    logger.info({"account": 123, "ip": "172.20.19.18"})
    logger.info("classic message for account: %s", account, extra={"account": account})
    
    try:
      h = {}
      h['key']
    except:
      logger.info("something unexpected happened", exc_info=True)

Sample output
-------------

The following keys will be found in the output JSON:

* ``@source_host``: source hostname for the log
* ``@timestamp``: ISO 8601 timestamp
* ``@message``: short message for this log
* ``@fields``: all extra fields

::

  {
    "@fields": {
        "account": "pyr",
        "args": [],
        "created": 1367480388.013037,
        "exception": [
            "Traceback (most recent call last):\n",
            "  File \"toto.py\", line 16, in <module>\n    k['unknown']\n",
            "KeyError: 'unknown'\n"
        ],
        "filename": "toto.py",
        "funcName": "<module>",
        "levelname": "WARNING",
        "levelno": 30,
        "lineno": 18,
        "module": "toto",
        "msecs": 13.036966323852539,
        "name": "root",
        "pathname": "toto.py",
        "process": 1819,
        "processName": "MainProcess",
        "relativeCreated": 18.002986907958984,
        "thread": 140060726359808,
        "threadName": "MainThread"
    },
    "@message": "TOTO",
    "@source_host": "phoenix.spootnik.org",
    "@timestamp": "2013-05-02T09:39:48.013158"
  }

