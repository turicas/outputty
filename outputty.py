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
import datetime
import re
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
                 input_encoding='utf8', output_encoding='utf8', from_csv='',
                 convert_types=True, order_by='', ordering=''):
        self.headers = headers if headers is not None else []
        self.dash = dash
        self.pipe = pipe
        self.plus = plus
        self.input_encoding = input_encoding
        self.output_encoding = output_encoding
        self.csv_filename = None
        self.rows = []
        self.types = {}
        if from_csv:
            self.convert_types = convert_types
            self._import_from_csv(from_csv)
        self.order_by_column = order_by
        self.ordering = ordering

    def order_by(self, column, ordering='asc'):
        index = self.headers.index(column)
        if ordering.lower().startswith('desc'):
            sort_function = lambda x, y: cmp(y[index], x[index])
        else:
            sort_function = lambda x, y: cmp(x[index], y[index])
        self.rows.sort(sort_function)

    def normalize_structure(self):
        result = []
        for row in self.rows:
            if isinstance(row, dict):
                row_data = []
                for header_name in self.headers:
                    if header_name not in row:
                        row[header_name] = None
                    row_data.append(row[header_name])
            else:
                row_data = list(row)
            result.append(row_data)
        self.rows = result

    def _str_decode(self, element, codec):
        if isinstance(element, str):
            return element.decode(codec)
        else:
            return element

    def _unicode_encode(self, element, codec):
        if isinstance(element, unicode):
            return element.encode(codec)
        else:
            return element

    def encode(self, codec=None):
        if codec is None:
            codec = self.output_encoding
        self.headers = [self._unicode_encode(x, codec) for x in self.headers]
        rows = []
        for row in self.rows:
            rows.append([self._unicode_encode(value, codec) for value in row])
        self.rows = rows

    def decode(self, codec=None):
        if codec is None:
            codec = self.input_encoding
        rows = []
        for row in self.rows:
            rows.append([self._str_decode(v, codec) for v in row])
        self.rows = rows
        self.headers = [self._str_decode(h, codec) for h in self.headers]

    def _organize_data(self):
        self.normalize_structure()
        self.decode()
        if self.order_by_column:
            self.order_by(self.order_by_column, self.ordering)

    def _define_maximum_column_sizes(self):
        self.max_size = {}
        for header in self.headers:
            if not isinstance(header, unicode):
                header = str(header)
            self.max_size[header] = len(header)
        for index, column in enumerate(zip(*self.rows)):
            sizes = []
            for value in column:
                if value is None:
                    value = ''
                sizes.append(len(unicode(value)))
            max_size = max(sizes)
            if max_size > self.max_size[self.headers[index]]:
                self.max_size[self.headers[index]] = max_size

    def _make_line_from_row_data(self, row_data):
        return '%s %s %s' % (self.pipe, (' %s ' % self.pipe).join(row_data),
                             self.pipe)

    def __unicode__(self):
        self._organize_data()
        self._define_maximum_column_sizes()
        if not len(self.headers) and not len(self.rows):
            return unicode()

        dashes = []
        centered_headers = []
        for header in self.headers:
            if not isinstance(header, unicode):
                header = str(header)
            dashes.append(self.dash * (self.max_size[header] + 2))
            centered_headers.append(header.center(self.max_size[header]))
        split_line = self.plus + self.plus.join(dashes) + self.plus
        header_line = self._make_line_from_row_data(centered_headers)

        result = [split_line, header_line, split_line]
        for row in self.rows:
            row_data = []
            for i, info in enumerate(row):
                if info is None:
                    info = ''
                data = unicode(info).rjust(self.max_size[self.headers[i]])
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
            if self.convert_types:
                self.normalize_types()

    def to_list_of_dicts(self):
        rows = []
        for row in self.rows:
            if isinstance(row, dict):
                rows.append(row)
            else:
                rows.append(dict(zip(self.headers, row)))
        return rows

    def _identify_type_of_data(self):
        columns = zip(*self.rows)
        date_regex = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
        datetime_regex = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2} '
                                    '[0-9]{2}:[0-9]{2}:[0-9]{2}$')
        for i, header in enumerate(self.headers):
            column_types = [int, float, datetime.date, datetime.datetime, str]
            cant_be = set()
            try:
                column = columns[i]
            except IndexError:
                self.types[header] = str
            else:
                for value in column:
                    if value == '':
                        value = None
                    try:
                        converted = int(value)
                        if str(converted) != str(value):
                            raise ValueError('It is float')
                    except ValueError:
                        cant_be.add(int)
                    except TypeError:
                        pass #None should pass
                    try:
                        converted = float(value)
                    except ValueError:
                        cant_be.add(float)
                    except TypeError:
                        pass #None should pass
                    if value is not None:
                        if datetime_regex.match(unicode(value)) is None:
                            cant_be.add(datetime.datetime)
                        if date_regex.match(unicode(value)) is None:
                            cant_be.add(datetime.date)
                for removed_type in cant_be:
                    column_types.remove(removed_type)
                self.types[header] = column_types[0]

    def normalize_types(self):
        self._identify_type_of_data()
        rows_converted = []
        for row in self.rows:
            row_data = []
            for index, value in enumerate(row):
                type_ = self.types[self.headers[index]]
                if value is None or value == '':
                    row_data.append(None)
                elif type_ == datetime.date:
                    info = [int(x) for x in value.split('-')]
                    row_data.append(datetime.date(*info))
                elif type_ == datetime.datetime:
                    info = value.split()
                    date = [int(x) for x in info[0].split('-')]
                    rest = [int(x) for x in info[1].split(':')]
                    row_data.append(datetime.datetime(*(date + rest)))
                elif type_ == str:
                    if isinstance(value, unicode):
                        row_data.append(value)
                    else:
                        if not isinstance(value, str):
                            value = str(value)
                        row_data.append(value.decode(self.input_encoding))
                else:
                    row_data.append(type_(value))
            rows_converted.append(row_data)
        self.rows = rows_converted

    def to_csv(self, filename):
        self._organize_data()
        encoded_headers = [x.encode(self.output_encoding) for x in self.headers]
        encoded_rows = [[info.encode(self.output_encoding) for info in row] \
                        for row in self.rows]
        encoded_data = [encoded_headers] + encoded_rows
        fp = open(filename, 'w')
        writer = csv.writer(fp, dialect=MyCSV)
        writer.writerows(encoded_data)
        fp.close()

    def to_text_file(self, filename):
        self._organize_data()
        fp = open(filename, 'w')
        fp.write(self.__str__())
        fp.close()

    def to_dict(self, only=None, key=None, value=None):
        self._organize_data()
        self.encode()
        table_dict = {}
        if key is not None and value is not None:
            if isinstance(key, str):
                key = key.decode(self.input_encoding)
            key = key.encode(self.output_encoding)
            if isinstance(value, str):
                value = value.decode(self.input_encoding)
            value = value.encode(self.output_encoding)
            key_index = self.headers.index(key)
            value_index = self.headers.index(value)
            for row in self.rows:
                table_dict[row[key_index]] = row[value_index]
        else:
            for index, column in enumerate(zip(*self.rows)):
                header_name = self.headers[index]
                if only is None or header_name in only:
                    table_dict[header_name] = list(column)
        self.decode(self.output_encoding)
        return table_dict

    def _to_html_unicode(self):
        self._organize_data()
        if self.css_classes:
            result = ['<table>', '  <tr class="header">']
        else:
            result = ['<table>', '  <tr>']
        for header in self.headers:
            result.append('    <th>%s</th>' % header)
        result.append('  </tr>')

        i = 1
        for row in self.rows:
            if self.css_classes:
                result.append('  <tr class="%s">' % \
                              ('odd' if i % 2 else 'even'))
            else:
                result.append('  <tr>')
            for value in row:
                if value is None:
                    value = ''
                result.append('    <td>%s</td>' % value)
            result.append('  </tr>')
            i += 1
        result.append('</table>')
        return '\n'.join(result)

    def to_html(self, filename='', css_classes=True):
        self.css_classes = css_classes
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
