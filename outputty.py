#!/usr/bin/env python
# coding: utf-8

# Copyright 2011 Álvaro Justen
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv


class MyCSV(csv.Dialect):
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_ALL


class Table(object):
    def __init__(self, headers=[], dash='-', pipe='|', plus='+',
                 input_encoding='utf8', output_encoding='utf8', from_csv=None):
        self.headers = headers
        self.dash = dash
        self.pipe = pipe
        self.plus = plus
        self.input_encoding = input_encoding
        self.output_encoding = output_encoding
        self.rows = []
        if from_csv:
            self.import_from_csv(from_csv)


    def construct_data(self):
        result = []
        result.append([x.decode(self.input_encoding) for x in self.headers])
        for row in self.rows:
            if isinstance(row, dict):
                row_data = []
                for header_name in self.headers:
                    if header_name in row:
                        if not isinstance(row[header_name], (str, unicode)):
                            data = unicode(row[header_name])
                        else:
                            data = row[header_name].decode(self.input_encoding)
                    else:
                        data = unicode()
                    row_data.append(data)
            else:
                row_data = []
                for info in row:
                    if not isinstance(info, (str, unicode)):
                        row_data.append(unicode(info))
                    else:
                        row_data.append(info.decode(self.input_encoding))
            result.append(row_data)
        self.data = result

    
    def __str__(self):
        self.construct_data()
        max_sizes = {}
        for column in zip(*self.data):
            max_sizes[column[0]] = max([len(x) for x in column])

        unicode_headers = [x.decode(self.input_encoding) for x in self.headers]
        dashes = [self.dash * (max_sizes[x] + 2) for x in unicode_headers]
        split_line = self.plus + self.plus.join(dashes) + self.plus
        headers_centralized = [x.center(max_sizes[x]) for x in unicode_headers]
        space_pipe_space = ' %s ' % self.pipe
        header_line = self.pipe + ' ' + \
                      space_pipe_space.join(headers_centralized) + ' ' + \
                      self.pipe

        result = [split_line, header_line, split_line]
        for row in self.data[1:]:
            row_data = []
            for i, info in enumerate(row):
                data = info.rjust(max_sizes[unicode_headers[i]])
                row_data.append(data)
            line = self.pipe + ' ' + space_pipe_space.join(row_data) + ' ' + \
                   self.pipe
            result.append(line)

        if self.rows:
            result.append(split_line)
        
        return '\n'.join([x.encode(self.output_encoding) for x in result])
    

    def import_from_csv(self, filename):
        fp = open(filename, 'r')
        reader = csv.reader(fp)
        data = [x for x in reader]
        fp.close()
        self.headers = data[0]
        self.rows = data[1:]


    def to_csv(self, filename):
        self.construct_data()
        encoded_data = []
        for row in self.data:
            row_data = []
            for info in row:
                row_data.append(info.encode(self.output_encoding))
            encoded_data.append(row_data)
        fp = open(filename, 'w')
        writer = csv.writer(fp, dialect=MyCSV)
        writer.writerows(encoded_data)
        fp.close()


    def to_text_file(self, filename):
        self.construct_data()
        fp = open(filename, 'w')
        fp.write(str(self))
        fp.close()

