#!/usr/bin/env python
# coding: utf-8

from outputty import Table

my_table = Table(headers=['First name', 'Last name'])
my_table.rows.append({'First name': 'Álvaro', 'Last name': 'Justen'})
my_table.rows.append(['Tatiana', 'Al-Chueyr'])
my_table.rows.append(('Flávio', 'Amieiro'))

my_table.to_csv('my-data.csv')
print my_table
