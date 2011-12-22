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
        table.headers = [x.decode('utf8') for x in table.data[0]]
        table.rows = [[y.decode('utf8') for y in x] for x in table.data[1:]]
        if table.convert_types:
            table.normalize_types()

def write(table, filename):
    table._organize_data()
    encoded_headers = [x.encode(table.output_encoding) for x in table.headers]
    encoded_rows = [[info.encode(table.output_encoding) for info in row] \
                    for row in table.rows]
    encoded_data = [encoded_headers] + encoded_rows
    fp = open(filename, 'w')
    writer = csv.writer(fp, dialect=MyCSV)
    writer.writerows(encoded_data)
    fp.close()
