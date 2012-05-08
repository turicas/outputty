#!/usr/bin/env python
# coding: utf-8
# title = Exporting to a CSV File
# output = 'my-data.csv', 'my-data.dsv'
#Using plugins we can import and export ``Table`` data to CSV (really, to and
#from a lot of formats). Let's create a simple table and export it to a CSV
#file.
#You can also create any kind of DSV (delimiter-separeted value) files, just
#passing ``delimiter``, ``quote_char`` and ``line_terminator`` to ``write`` (the
#same parameters apply to ``read``).

from outputty import Table

my_table = Table(headers=['First name', 'Last name'])
my_table.append({'First name': 'Álvaro', 'Last name': 'Justen'})
my_table.append(('Flávio', 'Amieiro'))
my_table.append(['Flávio', 'Coelho'])
my_table.write('csv', 'my-data.csv')

#Let's create a other kind of DSV:
my_table.write('csv', 'my-data.dsv', delimiter=';', quote_char="'",
        line_terminator='\r\n')
