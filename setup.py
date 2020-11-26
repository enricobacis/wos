from setuptools import setup
from sys import version_info

with open('README.rst') as README:
    long_description = README.read()
    long_description = long_description[long_description.index('Description'):]

with open('VERSION') as VERSION:
    version = VERSION.read().strip()

suds_install_requires = ['suds'] if version_info < (3, 0) else ['suds-py3']

setup(name='wos',
      version=version,
      description='Web of Science client using API v3.',
      long_description=long_description,
      install_requires=['limit'] + suds_install_requires,
      url='http://github.com/enricobacis/wos',
      author='Enrico Bacis',
      author_email='enrico.bacis@gmail.com',
      license='MIT',
      packages=['wos'],
      scripts=['scripts/wos'],
      keywords='wos isi web of science knowledge api client')
