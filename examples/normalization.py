#!/usr/bin/env python
# coding: utf-8

#A `Table` made with `dict`-like, `list`-like and `tuple`-like objects. For
#example, this code:

from outputty import Table
my_table = Table(headers=['First Name', 'Last Name', 'Main Language'])
my_table.append({'First Name': 'Álvaro', 'Last Name': 'Justen',
                      'Main Language': 'Python'})
my_table.append(('Flávio', 'Amieiro', 'Python'))

rows = my_table.to_list_of_dicts()
print rows[1]['First Name']

table_dict = my_table.to_dict()
print table_dict

table_dict_filtered = my_table.to_dict(only=['First Name', 'Last Name'])
print table_dict_filtered

other_table = Table(headers=['date', 'measure'])
other_table.append(('2011-12-01', 21))
other_table.append(('2011-12-02', 42))
other_table.append(('2011-12-03', 3.14))
other_table.append(('2011-12-04', 2.71))
values_as_dict = other_table.to_dict(key='date', value='measure')
print values_as_dict
