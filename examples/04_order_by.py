#!/usr/bin/env python
# coding: utf-8
# title = Ordering `Table` Data
#You can order your table's data with the method ``Table.order_by``.
#You need to specify a column in which the ordering will be based on and
#optionally specify if the ordering will be ascending (default) or descending.

from outputty import Table

my_table = Table(headers=['First name', 'Last name'])
my_table.append({'First name': 'Álvaro', 'Last name': 'Justen'})
my_table.append({'First name': 'Renne'})
my_table.append(('Flávio', 'Amieiro'))
my_table.order_by('Last name')
print my_table
