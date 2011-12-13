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

from __future__ import division
import csv
try:
    from numpy import histogram, ceil
except ImportError:
    pass


class MyCSV(csv.Dialect):
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_ALL


class Table(object):
    def __init__(self, headers=None, dash='-', pipe='|', plus='+',
                 input_encoding='utf8', output_encoding='utf8', from_csv=None):
        self.headers = headers if headers is not None else []
        self.dash = dash
        self.pipe = pipe
        self.plus = plus
        self.input_encoding = input_encoding
        self.output_encoding = output_encoding
        self.csv_filename = None
        self.rows = []
        if from_csv:
            self._import_from_csv(from_csv)

    def _convert_to_unicode(self, element):
        if isinstance(element, (str)):
            return element.decode(self.input_encoding)
        else:
            return unicode(element)

    def _organize_data(self):
        result = []
        result.append([self._convert_to_unicode(x) for x in self.headers])
        for row in self.rows:
            if isinstance(row, dict):
                row_data = []
                for header_name in self.headers:
                    if header_name not in row:
                        row[header_name] = ''
                    row_data.append(self._convert_to_unicode(row[header_name]))
            else:
                row_data = [self._convert_to_unicode(info) for info in row]
            result.append(row_data)
        self.data = result

    def _define_maximum_column_sizes(self):
        self.max_size = {}
        for column in zip(*self.data):
            self.max_size[column[0]] = max([len(x) for x in column])

    def _make_line_from_row_data(self, row_data):
        return '%s %s %s' % (self.pipe, (' %s ' % self.pipe).join(row_data),
                             self.pipe)

    def __unicode__(self):
        self._organize_data()
        if len(self.data) == 1 and not self.data[0]:
            return unicode()
        self._define_maximum_column_sizes()
        unicode_headers, rows = self.data[0], self.data[1:]

        dashes = [self.dash * (self.max_size[x] + 2) for x in unicode_headers]
        centered_headers = [x.center(self.max_size[x]) for x in unicode_headers]
        split_line = self.plus + self.plus.join(dashes) + self.plus
        header_line = self._make_line_from_row_data(centered_headers)

        result = [split_line, header_line, split_line]
        for row in rows:
            row_data = []
            for i, info in enumerate(row):
                data = info.rjust(self.max_size[unicode_headers[i]])
                row_data.append(data)
            result.append(self._make_line_from_row_data(row_data))
        if self.rows:
            result.append(split_line)
        return '\n'.join(result)

    def __str__(self):
        return self.__unicode__().encode(self.output_encoding)

    def _import_from_csv(self, file_name_or_pointer):
        if isinstance(file_name_or_pointer, (str, unicode)):
            self.csv_filename = file_name_or_pointer
            fp = open(file_name_or_pointer, 'r')
        else:
            fp = file_name_or_pointer
        self.fp = fp
        info = fp.read().decode(self.input_encoding).encode('utf8')
        reader = csv.reader(info.split('\n'))
        self.data = [x for x in reader if x]
        if self.csv_filename:
            fp.close()
        self.headers = []
        self.rows = []
        if self.data:
            self.headers = [x.decode('utf8') for x in self.data[0]]
            self.rows = [[y.decode('utf8') for y in x] for x in self.data[1:]]

    def to_list_of_dicts(self):
        rows = []
        for row in self.rows:
            if isinstance(row, dict):
                rows.append(row)
            else:
                rows.append(dict(zip(self.headers, row)))
        return rows

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

    def _to_html_unicode(self):
        self._organize_data()
        if len(self.data) == 1 and not self.data[0]:
            return unicode()
        unicode_headers, rows = self.data[0], self.data[1:]
        result = ['<table>', '  <tr>']
        for header in unicode_headers:
            result.append('    <th>%s</th>' % header)
        result.append('  </tr>')

        for row in rows:
            result.append('  <tr>')
            for value in row:
                result.append('    <td>%s</td>' % value)
            result.append('  </tr>')
        result.append('</table>')
        return '\n'.join(result)

    def to_html(self, filename=''):
        contents = self._to_html_unicode().encode(self.output_encoding)
        if not filename:
            return contents
        else:
            fp = open(filename, 'w')
            fp.write(contents)
            fp.close()


class Histogram(object):
    __author__ = "fccoelho"
    __date__ = "$12/10/2009 14:25:05$"
    __license__ = "GPL v3"
    __docformat__ = "restructuredtext en"

    """
    Ascii histogram
    """
    def __init__(self, data, bins=10):
        """
        Class constructor

        :Parameters:
            - `data`: array like object
        """
        self.data = data
        self.bins = bins
        self.h = histogram(self.data, bins=self.bins)

    def horizontal(self, height=4, character='|'):
        """Returns a multiline string containing a
        a horizontal histogram representation of self.data

        :Parameters:
            - `height`: Height of the histogram in characters
            - `character`: Character to use

        >>> d = normal(size=1000)
        >>> h = Histogram(d,bins=25)
        >>> print h.horizontal(5,'|')
        106            |||
                      |||||
                      |||||||
                    ||||||||||
                   |||||||||||||
        -3.42                         3.09
        """
        his = []
        bars = self.h[0] / max(self.h[0]) * height
        for l in reversed(range(1, height + 1)):
            line = ''
            if l == height:
                line = '%s ' % max(self.h[0]) #histogram top count
            else:
                line = ' ' * (len(str(max(self.h[0]))) + 1) #add leading spaces
            for c in bars:
                if c >= ceil(l):
                    line += character
                else:
                    line += ' '
            his.append(line.rstrip())
        his.append('%.2f%s%.2f' % (self.h[1][0], ' ' * self.bins,
                                   self.h[1][-1]))
        return '\n'.join(his)

    def vertical(self,height=20, character ='|'):
        """
        Returns a Multi-line string containing a
        a vertical histogram representation of self.data

        :Parameters:
            - `height`: Height of the histogram in characters
            - `character`: Character to use

        >>> d = normal(size=1000)
        >>> Histogram(d,bins=10)
        >>> print h.vertical(15,'*')
                              236
        -3.42:
        -2.78:
        -2.14: ***
        -1.51: *********
        -0.87: *************
        -0.23: ***************
        0.41 : ***********
        1.04 : ********
        1.68 : *
        2.32 :
        """
        his = []
        xl = ['%.2f' % n for n in self.h[1]]
        lxl = [len(l) for l in xl]
        bars = self.h[0] / max(self.h[0]) * height
        his.append(' ' * (max(bars) + 2 + max(lxl)) + '%s\n' % max(self.h[0]))
        for i, c in enumerate(bars):
            line = xl[i] + ' ' * (max(lxl) - lxl[i]) + ': ' + character * c
            his.append(line.rstrip())
        return '\n'.join(his)
