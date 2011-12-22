#!/usr/bin/env python
# coding: utf-8
# title = Basics of `Table`
#A `Table` is a list of rows. These rows can be represented with `dict`-like,
#`list`-like and `tuple`-like objects. Let's create one and prints it to
#stdout.

from outputty import Table
my_table = Table(headers=['First Name', 'Last Name', 'Main Language'])
my_table.rows.append({'First Name': 'Álvaro', 'Last Name': 'Justen',
                      'Main Language': 'Python'})
my_table.rows.append(('Flávio', 'Amieiro', 'Python'))
print my_table
