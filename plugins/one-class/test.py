#!/usr/bin/env python

from outputty import Table


my_table = Table()
my_table.data = [5, 4, 3, 2, 1]
my_table.sort()
my_table.write('show')
my_table.write('file', 'test.txt')
print my_table.plugins

other_table = Table()
other_table.data = [5, 4, 3, 2, 1]
other_table.read('file', 'data.txt')
print other_table.data
print other_table.plugins
