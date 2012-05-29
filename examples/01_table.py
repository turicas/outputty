#!/usr/bin/env python
# coding: utf-8
# title = Basics of ``Table``
#A ``Table`` is simply a list of rows. These rows can be represented as
#``dict``-like, ``list``-like or ``tuple``-like objects. Let's create one
#``Table`` with some rows and print it to stdout.

from outputty import Table
my_table = Table(headers=['First Name', 'Last Name', 'Main Language'])
my_table.append({'First Name': 'Álvaro', 'Last Name': 'Justen',
                 'Main Language': 'Python'}) #appending row as dict
my_table.append(('Flávio', 'Amieiro', 'Python')) #appending row as tuple
my_table.append(['Flávio', 'Coelho', 'Python']) #appending row as list
print my_table
