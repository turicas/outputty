#!/usr/bin/env python

class Table(object):
    def __init__(self, data=None):
        self.data = data or [5, 4, 3, 2, 1]

    def sort(self):
        self.data.sort()
