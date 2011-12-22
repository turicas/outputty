#!/usr/bin/env python

from base_table import Table
from plugin_savefile import save_file
from plugin_show import show


my_table = Table()
print dir(my_table)

my_table.sort() #method of BaseClass
show(my_table)
save_file(my_table, 'test.txt')
