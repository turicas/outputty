#!/usr/bin/env python

from base_table import BaseTable


class SaveFileTable(BaseTable):
    def save_file(self, filename):
        fp = open(filename, 'w')
        fp.write('Your table contains:\n')
        for i in self.data:
            fp.write(' - %s\n' % str(i))
        fp.close()
