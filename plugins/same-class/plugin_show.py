#!/usr/bin/env python

from base_table import BaseTable


class PrintTable(BaseTable):
    def show(self):
        print 'Your data is: ', self.data
