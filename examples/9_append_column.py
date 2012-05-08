#!/usr/bin/env python
# coding: utf-8
# title = Appending a column
#You can append a column in your ``Table`` object using the ``append_column``
#method or just setting an item (``my_table['new-column'] = ...``). You can
#pass a list of values or a function to generate the values based on row data.
#Let's see how it works - it's quite simple.

from outputty import Table


table = Table(headers=['Name', 'Creation Year'])
table.append(['Python', 1991])
table.append(['Unix', 1969])

#We have the values, so we'll append it:
table.append_column('Category', ['Programming Language', 'Operating System'])
#Same effect for this line:
#table['Category'] = ['Programming Language', 'Operating System']

#We can also generate the values:
table.append_column('Age', lambda row: 2012 - row[1]) #row is a list
#Our function can receive row as dict (with `row_as_dict` parameter) and we
#can insert the column where we want (with `position` parameter):
table.append_column('First Letter', lambda row: row['Name'][0],
                    row_as_dict=True, position=0) #row is dict
#...and the result:
print table
