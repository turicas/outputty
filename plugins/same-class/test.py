#!/usr/bin/env python

from main import Table


my_table = Table()
print dir(my_table)

my_table.sort()
my_table.show()
my_table.save_file('test.txt')
