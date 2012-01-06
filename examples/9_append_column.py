#!/usr/bin/env python
# coding: utf-8
# title = Appending a column
#You can append a column in your `Table` object using the `append_column`
#method. Let's see how it works

from outputty import Table


table = Table(headers=['Name', 'Creation Year'])
table.append(['Python', 1991])
table.append(['Unix', 1969])

#We have the values, so we'll append it:
table.append_column('Category', ['Programming Language', 'Operating System'])

#We can also generate the values:
table.append_column('Age', lambda row: 2012 - row[1])
#Our function can receive row as dict (with `row_as_dict` parameter) and we
#can insert the column where we want (with `position` parameter):
table.append_column('First Letter', lambda row: row['Name'][0],
                    row_as_dict=True, position=0)

print table
