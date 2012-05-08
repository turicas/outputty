#!/usr/bin/env python
# coding: utf-8
# title = Using table columns and rows
#You can get an entire table column just getting the item ``column-name`` in
#your table object. You can also change and delete an entire column.
#If the item you get is a string, a column is returned. If it is an integer, a
#row is returned (starting from 0). ``Table`` objects are iterable, so you can
#navigate through the rows with a simple ``for`` loop.

from outputty import Table

table = Table(headers=['spam', 'eggs', 'ham'])
table.append(['python', 3.14, 1 + 5j])
table.append(['rules', 42, 3 + 4j])
del table['eggs']
print 'Table after deleting "eggs" column:'
print table
print '\nNow only column "spam":'
print table['spam']
print 'First row:'
print table[0]
print 'All rows:'
for index, row in enumerate(table):
    print '  Row #%d: %s' % (index, row)
table['ham'] = [1, 2] # Setting new values for this column
print 'Table after chaning an entire column:'
print table
