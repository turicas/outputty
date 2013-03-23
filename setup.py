#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup

setup(name='outputty',
    description='Import, filter and export tabular data with Python easily',
    long_description=open('README.rst').read(),
    version='0.3.2',
    author=u'Álvaro Justen',
    author_email='alvarojusten@gmail.com',
    url='https://github.com/turicas/outputty/',
    packages=['outputty'],
    install_requires=[],
    keywords=['data processing', 'data exchange', 'etl'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
