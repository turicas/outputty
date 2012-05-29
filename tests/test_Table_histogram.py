#!/usr/bin/env python
# coding: utf-8
"""
Tests for histogram module
"""
import unittest
from outputty import Table
from numpy.random import seed
from numpy.random import normal
from textwrap import dedent


class TestHistogram(unittest.TestCase):
    def test_vertical_histogram(self):
        seed(1234) # Setting the seed to get repeatable results
        numbers = normal(size=1000)
        my_table = Table(headers=['values'])
        my_table.extend([[value] for value in numbers])
        output = my_table.write('histogram', column='values', height=5,
                                orientation='vertical', bins=10)
        expected = dedent('''
        265      |
                 ||
                |||
                ||||
               ||||||
        -3.56          2.76
        ''').strip()
        self.assertEquals(output, expected)

    def test_horizontal_histogram(self):
        seed(1234) # Setting the seed to get repeatable results
        numbers = normal(size=1000)
        my_table = Table(headers=['values'])
        my_table.extend([[value] for value in numbers])
        output = my_table.write('histogram', column='values', height=15, bins=10,
                                orientation='horizontal')
        expected = dedent('''\
                              265

        -3.56:
        -2.93:
        -2.30: ||
        -1.67: ||||
        -1.03: ||||||||||
        -0.40: |||||||||||||||
        0.23 : ||||||||||||
        0.87 : ||||||
        1.50 : |||
        2.13 :''')
        self.assertEquals(output, expected)
