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

def read(table, file_name_or_pointer, convert_types=True):
    table.convert_types = convert_types
    if isinstance(file_name_or_pointer, (str, unicode)):
        table.csv_filename = file_name_or_pointer
        fp = open(file_name_or_pointer, 'r')
    else:
        fp = file_name_or_pointer
    table.fp = fp
    info = fp.read().decode(table.input_encoding).encode('utf8')
    reader = csv.reader(info.split('\n'))
    table.data = [x for x in reader if x]
    if table.csv_filename:
        fp.close()
    table.headers = []
    table.rows = []
    if table.data:
        table.headers = table.data[0]
        table.rows = table.data[1:]
        table.decode('utf-8')
        if table.convert_types:
            table.normalize_types()

def write(table, filename):
    table.decode()
    table.encode()
    encoded_data = [[str(x) for x in table.headers]] + \
                   [[str(v) for v in row] for row in table.rows]
    print encoded_data
    fp = open(filename, 'w')
    writer = csv.writer(fp, dialect=MyCSV)
    writer.writerows(encoded_data)
    fp.close()
    table.decode(table.output_encoding)
