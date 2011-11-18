#!/usr/bin/env python
# coding: utf-8
"""
Tests for Asciihist module
"""
import unittest
from asciihist import Histogram
from numpy.random import seed
from numpy.random import normal

# Setting the seed to get repeatable results


class TestTableTxt(unittest.TestCase):
    def test_horizontal_hist(self):
        seed(1234)# Setting the seed to get repeatable results
        d = normal(size=1000)
        h = Histogram(d,bins=10)
        expected = "265      |    \n         ||   \n        |||   \n        ||||  \n       |||||| \n-3.56          2.76\n"
        self.assertEquals(h.horizontal(5),expected)

    def test_vertical_hist(self):
        seed(1234)# Setting the seed to get repeatable results
        d = normal(size=1000)
        h = Histogram(d,bins=10)
        expected = "                      265\n-3.56: \n-2.93: \n-2.30: ||\n-1.67: ||||\n-1.03: ||||||||||\n-0.40: |||||||||||||||\n0.23 : ||||||||||||\n0.87 : ||||||\n1.50 : |||\n2.13 : \n"""
        self.assertEquals(h.vertical(15), expected)