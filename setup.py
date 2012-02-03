#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup

setup(name='outputty',
      description='Import, filter and export tabular data with Python easily',
      long_description=open('long_description.txt').read(),
      version='0.2.0a',
      author='Álvaro Justen'.decode('utf-8'),
      author_email='alvarojusten@gmail.com',
      url='https://github.com/turicas/outputty/',
      download_url='https://github.com/turicas/outputty/tarball/0.2.0a',
      packages=['outputty'],
      keywords=['data processing', 'data exchange', 'etl'],
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ]
)
