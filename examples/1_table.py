#!/usr/bin/env python
# coding: utf-8

from outputty import Table
my_table = Table(headers=['First name', 'Last name'])
my_table.rows.append({'First name': 'Álvaro', 'Last name': 'Justen'})
my_table.rows.append(('Flávio', 'Amieiro'))
print my_table

rows = my_table.to_list_of_dicts()
print rows[1]['First name']

my_table.normalize()
print my_table.rows
