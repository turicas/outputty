#!/usr/bin/env python
# coding: utf-8

def write(table, filename_or_pointer=None):
    contents = str(table) + '\n'
    if filename_or_pointer is None:
        return contents
    else:
        if isinstance(filename_or_pointer, (str, unicode)):
            fp = open(filename_or_pointer, 'w')
            close = True
        else:
            fp = filename_or_pointer
            close = False
        table._organize_data()
        fp.write(contents)
        if close:
            fp.close()
