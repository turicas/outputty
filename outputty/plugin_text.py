#!/usr/bin/env python
# coding: utf-8

def write(table, filename=None):
    if filename is None:
        return str(table)
    else:
        table._organize_data()
        fp = open(filename, 'w')
        fp.write(str(table))
        fp.close()
