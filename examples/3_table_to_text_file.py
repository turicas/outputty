#!/usr/bin/env python
# coding: utf-8
# title = Exporting to a Text File
# input = 'nice-software.csv', code
# output = 'nice-software.txt'
#We can also import data from a CSV file and export it to a text file (using
#plugins, again).

from outputty import Table

my_table = Table()
my_table.read('csv', 'nice-software.csv')
my_table.write('text', 'nice-software.txt')
