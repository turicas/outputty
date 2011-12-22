#!/usr/bin/env python

def _transform(data):
    return ', '.join([str(x) for x in data])

def write(table):
    '''Writes `table.data` to stdout'''
    print 'Your data is: ', _transform(table.data)
