#!/usr/bin/env python

def _transform(data):
    return ', '.join([str(x) for x in data])

def out(table):
    print 'Your data is: ', _transform(table.data)
