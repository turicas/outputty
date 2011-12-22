#!/usr/bin/env python

from outputty import Table


my_table = Table()
print dir(my_table)

my_table.sort()
my_table.out('show')
my_table.out('savefile', 'test.txt')
