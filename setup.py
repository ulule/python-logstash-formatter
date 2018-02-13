import codecs
import unittest

from setuptools import setup, find_packages
from os import path

def read(*parts):
    return codecs.open(path.join(path.dirname(__file__), *parts),
                       encoding="utf-8").read()


def tests_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(name='logstash_formatter',
      version='0.5.17',
      description='JSON formatter meant for logstash',
      long_description=read('README.rst'),
      url='https://github.com/exoscale/python-logstash-formatter',
      author='Pierre-Yves Ritschard',
      author_email='pierre-yves.ritschard@exoscale.ch',
      license='MIT, see LICENSE file',
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3'
      ],
      zip_safe=False,
      test_suite='setup.tests_suite')
