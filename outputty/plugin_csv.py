#!/usr/bin/env python
# coding: utf-8

import csv


class MyCSV(csv.Dialect):
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_ALL

def read(table, filename_or_pointer, convert_types=True):
    if isinstance(filename_or_pointer, (str, unicode)):
        fp = open(filename_or_pointer, 'r')
        close = True
    else:
        fp = filename_or_pointer
        close = False
    info = fp.read().decode(table.input_encoding).encode('utf8')
    reader = csv.reader(info.split('\n'))
    data = [x for x in reader if x]
    table.headers = []
    table.rows = []
    if data:
        table.headers = data[0]
        table.rows = data[1:]
        table.decode('utf-8')
        if convert_types:
            table.normalize_types()
    if close:
        fp.close()

def write(table, filename_or_pointer):
    table.decode()
    table.encode()
    if isinstance(filename_or_pointer, (str, unicode)):
        fp = open(filename_or_pointer, 'w')
        close = True
    else:
        fp = filename_or_pointer
        close = False
    writer = csv.writer(fp, dialect=MyCSV)
    writer.writerow(table.headers)
    writer.writerows(table.rows)
    table.decode(table.output_encoding)
    if close:
        fp.close()
