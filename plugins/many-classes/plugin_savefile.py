#!/usr/bin/env python

def save_file(table, filename):
    fp = open(filename, 'w')
    fp.write('Your table contains:\n')
    for i in table.data:
        fp.write(' - %s\n' % str(i))
    fp.close()
