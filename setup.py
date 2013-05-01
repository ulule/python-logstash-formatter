from setuptools import setup, find_packages

setup(name='logstash_formatter',
      version='0.5.0',
      description='JSON formatter meant for logstash',
      url='https://github.com/exoscale/python-logstash-formatter',
      author='Exoscale',
      author_email='ops@exoscale.ch',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
