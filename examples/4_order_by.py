#!/usr/bin/env python
# coding: utf-8

from outputty import Table
my_table = Table(headers=['First name', 'Last name'], order_by='Last name')
my_table.rows.append({'First name': 'Álvaro', 'Last name': 'Justen'})
my_table.rows.append({'First name': 'Renne'})
my_table.rows.append(('Flávio', 'Amieiro'))
print my_table

my_table = Table(headers=['Programming Languages'])
my_table.rows.extend([['Python'], ['Bash scripting'], ['C']])
my_table.order_by('Programming Languages') #ordering = 'asc' by default
print my_table

