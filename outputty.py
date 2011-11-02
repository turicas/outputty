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


    def _convert_to_unicode(self, element):
        if not isinstance(element, (str, unicode)):
            return unicode(element)
        else:
            return element.decode(self.input_encoding)


    def _organize_data(self):
        result = []
        result.append([x.decode(self.input_encoding) for x in self.headers])
        for row in self.rows:
            if isinstance(row, dict):
                row_data = []
                for header_name in self.headers:
                    if header_name in row:
                        data = self._convert_to_unicode(row[header_name])
                    else:
                        data = unicode()
                    row_data.append(data)
            else:
                row_data = [self._convert_to_unicode(info) for info in row]
            result.append(row_data)
        self.data = result


    def _define_maximum_column_sizes(self):
        self.max_sizes = {}
        for column in zip(*self.data):
            self.max_sizes[column[0]] = max([len(x) for x in column])
    
    def __unicode__(self):
        self._organize_data()
        self._define_maximum_column_sizes()

        unicode_headers = self.data[0]
        dashes = [self.dash * (self.max_sizes[x] + 2) for x in unicode_headers]
        split_line = self.plus + self.plus.join(dashes) + self.plus
        headers_centralized = [x.center(self.max_sizes[x]) \
                               for x in unicode_headers]
        space_pipe_space = ' %s ' % self.pipe
        header_line = self.pipe + ' ' + \
                      space_pipe_space.join(headers_centralized) + ' ' + \
                      self.pipe

        result = [split_line, header_line, split_line]
        for row in self.data[1:]:
            row_data = []
            for i, info in enumerate(row):
                data = info.rjust(self.max_sizes[unicode_headers[i]])
                row_data.append(data)
            result.append('%s %s %s' % (self.pipe,
                                        space_pipe_space.join(row_data),
                                        self.pipe))
        if self.rows:
            result.append(split_line)
        return '\n'.join(result)


    def __str__(self):
        return self.__unicode__().encode(self.output_encoding)
    

    def import_from_csv(self, filename):
        fp = open(filename, 'r')
        reader = csv.reader(fp)
        data = list(reader) #reader is an iterator
        fp.close()
        self.headers = data[0]
        self.rows = data[1:]


    def to_csv(self, filename):
        self._organize_data()
        encoded_data = [[info.encode(self.output_encoding) for info in row] \
                        for row in self.data]
        fp = open(filename, 'w')
        writer = csv.writer(fp, dialect=MyCSV)
        writer.writerows(encoded_data)
        fp.close()


    def to_text_file(self, filename):
        self._organize_data()
        fp = open(filename, 'w')
        fp.write(self.__str__())
        fp.close()
