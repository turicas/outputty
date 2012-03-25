#!/usr/bin/env python
# coding: utf-8
# title = Exporting to a Text File
# input = 'nice-software.csv', code
# output = 'nice-software.txt'
#We can also import data from a CSV file and export it to a text file (using
#plugins, again). The data written to the text file will be the same we saw
#when executed ``print my_table`` in Example 1.

from outputty import Table

my_table = Table()
my_table.read('csv', 'nice-software.csv')
my_table.write('text', 'nice-software.txt')
