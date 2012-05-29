#!/usr/bin/env python
# coding: utf-8
# title = Other `Table` methods
#A ``Table`` is implemented as a list of rows with some methods to use plugins,
#ordering and do other things. ``Table`` have all operations/methods other
#Python mutable sequence objects have so you can use slicing,
#``Table.extend``, ``Table.index``, ``Table.count`` and so on. The exception is
#``sort`` (``Table`` have ``order_by`` instead).
#Read more:
#`mutable sequence operations <http://docs.python.org/library/stdtypes.html#mutable-sequence-types>`_.
#
#.. Note: all these methods support `tuple`, `list` or `dict` notations of row.

from outputty import Table

table = Table(headers=['City', 'State', 'Country'])
table.append(['Três Rios', 'Rio de Janeiro', 'Brazil'])
table.append(['Niterói', 'Rio de Janeiro', 'Brazil'])
table.append(['Rio de Janeiro', 'Rio de Janeiro', 'Brazil'])
table.append(['Porto Alegre', 'Rio Grande do Sul', 'Brazil'])
table.append(['São Paulo', 'São Paulo', 'Brazil'])

print 'First 3 rows:'
for row in table[:3]: # Slicing
    print row

#Change the two last rows:
table[-2:] = [['Junín', 'Buenos Aires', 'Argentina'],
              ['Ciudad del Este', 'Alto Paraná', 'Paraguay']]
#Insert a row in the first position, using dict notation:
table.insert(0, {'City': 'La Paz', 'State': 'La Paz', 'Country': 'Bolivia'})
print 'New table:'
print table
print

table.reverse()
print 'And the table in the reversed order:'
print table
print

popped_row = table.pop()
rio = ['Rio de Janeiro', 'Rio de Janeiro', 'Brazil']
table.append(rio) #repeated row
number_of_rios = table.count(rio)
index_of_first_rio = table.index(rio)
table.remove(rio) #remove the first occurrence of this row
number_of_rows = len(table)
print 'Popped row:', popped_row
print 'Number of rows:', number_of_rows
print 'Count of Rios rows (before remove):', number_of_rios
print 'Table after pop and remove:'
print table
print

#Removing non-brazilian cities:
del table[:2]
#Let's change an entire column:
table['Country'] = ['Brasil', 'Brasil', 'Brasil']
print 'Column "Country" changed:'
print table
