#!/usr/bin/env python
# coding: utf-8

from numpy.random import normal
from numpy.random import seed
from outputty import Histogram

seed(1234)
distribution = normal(size=1000)
my_histogram = Histogram(distribution, bins=10)
print 'Vertical:'
print my_histogram.vertical(15)
print
print 'Horizontal:'
print my_histogram.horizontal(5)
