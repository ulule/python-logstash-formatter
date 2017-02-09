logstash_formatter: JSON logs for logstash
==========================================

This library is provided to allow standard python logging to output log data
as json objects ready to be shipped out to logstash.

This project has been originally open sourced by `exoscale <https://www.exoscale.ch/>`_ (which is a great hosting service btw), thanks to them.

Installing
----------
Pip (`PyPI`_)::

    pip install logstash_formatter

.. _PyPI: https://pypi.python.org/pypi/logstash_formatter

Manual::

    python setup.py install

Usage
-----

Json outputs are provided by the LogstashFormatter logging formatter.

::

    import logging
    from logstash_formatter import LogstashFormatterV1

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = LogstashFormatterV1()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

The LogstashFormatter may take the following named parameters:

* ``fmt``: Config as a JSON string that supports:

  * ``extra``: provide extra fields always present in logs.
  * ``source_host``: override source host name.

* ``json_cls``: JSON encoder to forward to ``json.dump``.
* ``json_default``: Default JSON representation for unknown types,
  by default coerce everything to a string.

``LogstashFormatterV1`` adheres to the more 1.2.0 schema and will not update
fields, apart from a special handling of ``msg`` which will be updated to
``message`` when applicable.

You can also add extra fields to your json output by specifying a dict in place of message, or by specifying
the named argument ``extra`` as a dictionary. When supplying the ``exc_info`` named argument with a truthy value,
and if an exception is found on the stack, its traceback will be attached to the payload as well.

::

    logger.info({"account": 123, "ip": "172.20.19.18"})
    logger.info("classic message for account: {account}", extra={"account": account})
    
    try:
      h = {}
      h['key']
    except:
      logger.info("something unexpected happened", exc_info=True)

Sample output for LogstashFormatter
-----------------------------------

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
            "  File \"test.py\", line 16, in <module>\n    k['unknown']\n",
            "KeyError: 'unknown'\n"
        ],
        "filename": "test.py",
        "funcName": "<module>",
        "levelname": "WARNING",
        "levelno": 30,
        "lineno": 18,
        "module": "test",
        "msecs": 13.036966323852539,
        "name": "root",
        "pathname": "test.py",
        "process": 1819,
        "processName": "MainProcess",
        "relativeCreated": 18.002986907958984,
        "thread": 140060726359808,
        "threadName": "MainThread"
    },
    "@message": "TEST",
    "@source_host": "phoenix.spootnik.org",
    "@timestamp": "2013-05-02T09:39:48.013158"
  }


Sample output for LogstashFormatterV1
-------------------------------------

The following keys will be found in the output JSON:

* ``@timestamp``: ISO 8601 timestamp
* ``@version``: Version of the schema

::

    {"@version": 1,
     "account": "pyr",
     "lineno": 1,
     "levelno": 30,
     "filename": "test.py",
     "thread": 140566036444928,
     "@timestamp": "2015-03-30T09:46:23.000Z",
     "threadName": "MainThread",
     "relativeCreated": 51079.52117919922,
     "process": 10787,
     "source_host": "phoenix.spootnik.org",
     "processName": "MainProcess",
     "pathname": "test.py",
     "args": [],
     "module": "test",
     "msecs": 999.9005794525146,
     "created": 1427708782.9999006,
     "name": "root",
     "stack_info": null,
     "funcName": "<module>",
     "levelname": "WARNING",
     "message": "foo"}
