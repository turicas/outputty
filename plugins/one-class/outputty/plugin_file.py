#!/usr/bin/env python

'''plugin_file can save and load Table.data from/to a file'''

def write(table, filename):
    '''This function writes all contents of `table.data` to a file called
    `filename`'''
    fp = open(filename, 'w')
    for i in table.data:
        fp.write('%s\n' % str(i))
    fp.close()

def read(table, filename):
    '''This function reads the contents of a file called `filename` and loads
    it into `table.data`'''
    table.data = []
    fp = open(filename)
    for line in fp:
        table.data.append(line.strip())
    fp.close()
