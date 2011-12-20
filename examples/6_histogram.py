#!/usr/bin/env python
# coding: utf-8

from numpy.random import normal
from numpy.random import seed
from outputty import Table

seed(1234)
distribution = normal(size=1000)
my_table = Table(headers=['numbers'])
my_table.rows.extend([[value] for value in distribution])
print 'Vertical:'
print my_table.to_histogram('numbers', 'vertical', bins=10, height=7)
print
print 'Horizontal:'
print my_table.to_histogram('numbers', 'horizontal', bins=10, height=7,
                            character='#')
