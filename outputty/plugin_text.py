#!/usr/bin/env python
# coding: utf-8

def write(table, filename=None):
    if filename is None:
        return str(table)
    else:
        fp = open(filename, 'w')
        fp.write(str(table))
        fp.close()
