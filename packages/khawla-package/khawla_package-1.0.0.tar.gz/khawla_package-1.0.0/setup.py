from setuptools import setup

setup(
   name='khawla_package',
   version='1.0.0',
   author='khawla senkadi',
   author_email='k.senkadi@esi-sba.dz',
   packages=['khawla_package'],
   url='http://pypi.python.org/pypi/khawla_package/',
   license='LICENSE.txt',
   description='An awesome package that does something',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   install_requires=['khawla_package']
)