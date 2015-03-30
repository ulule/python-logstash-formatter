import codecs
from setuptools import setup, find_packages
from os import path

def read(*parts):
    return codecs.open(path.join(path.dirname(__file__), *parts),
                       encoding="utf-8").read()

setup(name='logstash_formatter',
      version='0.5.12',
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
      zip_safe=False)
