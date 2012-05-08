#!/usr/bin/env python
# coding: utf-8
# title = Creating Histograms
#There is a plugin called ``histogram`` that is shipped by default with
#``outputty`` - it can create histograms of your table's columns (using
#``numpy``). The output will be the histogram represented as text.

from numpy.random import normal
from numpy.random import seed
from outputty import Table

seed(1234)
distribution = normal(size=1000)
my_table = Table(headers=['numbers'])
my_table.extend([[value] for value in distribution])
print 'Vertical:'
print my_table.write('histogram', 'numbers', 'vertical', bins=10, height=7)
print
print 'Horizontal:'
print my_table.write('histogram', 'numbers', 'horizontal', bins=10, height=7,
                     character='#')
