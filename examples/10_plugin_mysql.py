#!/usr/bin/env python
# coding: utf-8
# title = Using MySQL plugin
#It's easy to import data from and export data to a MySQL table.
#``outputty`` automatically identify type of data and creates a table in MySQL
#for you with correct data types, so don't worry about converting everyting.
#Let's create a simple table, export it to MySQL and then import it again.
#Note: you need to change ``connection_string`` before run it.

from outputty import Table
from random import randint


# The connection string should be in the format:
#  'username:password@server[:port]/database/table_name'
connection_string = 'root:r00t@localhost/testing/test_table_' + \
                    str(randint(0, 99999))
my_table = Table(headers=['ID', 'First name', 'Last name'])
my_table.append({'First name': 'Álvaro', 'Last name': 'Justen', 'ID': '123'})
my_table.append((456, 'Flávio', 'Amieiro'))
my_table.append(['789', 'Flávio', 'Coelho'])
my_table.write('mysql', connection_string)
print 'Table saved:'
print my_table
print 'The types identified are:', my_table.types

other_table = Table()
other_table.read('mysql', connection_string)
print
print 'Table retrieved:'
print other_table
