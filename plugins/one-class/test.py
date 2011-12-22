#!/usr/bin/env python

from outputty import Table


my_table = Table()
print dir(my_table)

my_table.sort()
my_table.write('show')
my_table.write('file', 'test.txt')

other_table = Table()
other_table.read('file', 'data.txt')
print other_table.data
