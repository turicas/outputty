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

"""`outputty` is a simple Python library that helps you importing, filtering and
exporting data. It is composed by a main `Table` class and a lot of plugins
that helps importing and exporting data to/from `Table` (in future we'll have
filtering plugins). You can write your own plugin easily (see
`outputty/plugin_*.py` for examples).

Some examples of plugins are: CSV, text, HTML and histogram.
"""

import datetime
import re
import types
from collections import Counter


def _str_decode(element, codec):
    if isinstance(element, str):
        return element.decode(codec)
    else:
        return element


def _unicode_encode(element, codec):
    if isinstance(element, unicode):
        return element.encode(codec)
    else:
        return element


class Table(object):
    def __init__(self, headers=None, dash='-', pipe='|', plus='+',
                 input_encoding='utf8', output_encoding='utf8'):
        self.headers = headers if headers is not None else []
        for header in self.headers:
            if not isinstance(header, (str, unicode)):
                raise ValueError('Headers must be strings.')
        else:
            if len(self.headers) != len(set(self.headers)):
                raise ValueError('Header names must be unique.')
        self.headers = [_str_decode(h, input_encoding) for h in self.headers]
        self.dash = dash
        self.pipe = pipe
        self.plus = plus
        self.input_encoding = input_encoding
        self.output_encoding = output_encoding
        self.csv_filename = None
        self._rows = []
        self.types = {}
        self.plugins = {}

    def __setitem__(self, item, value):
        if isinstance(item, (str, unicode)):
            if item not in self.headers:
                self.append_column(item, value)
            columns = zip(*self._rows)
            if not columns or len(value) != len(self):
                raise ValueError
            else:
                columns[self.headers.index(item)] = value
                self._rows = [list(x) for x in zip(*columns)]
        elif isinstance(item, int):
            self._rows[item] = self._prepare_to_append(value)
        elif isinstance(item, slice):
            self._rows[item] = [self._prepare_to_append(v) for v in value]
        else:
            raise ValueError

    def __getitem__(self, item):
        if isinstance(item, (str, unicode)):
            if item not in self.headers:
                raise KeyError
            columns = zip(*self._rows)
            if not columns:
                return []
            else:
                return list(columns[self.headers.index(item)])
        elif isinstance(item, (int, slice)):
            return self._rows[item]
        else:
            raise ValueError

    def __delitem__(self, item):
        if isinstance(item, (str, unicode)):
            columns = zip(*self._rows)
            header_index = self.headers.index(item)
            del columns[header_index]
            del self.headers[header_index]
            self._rows = [list(row) for row in zip(*columns)]
        elif isinstance(item, (int, slice)):
            del self._rows[item]
        else:
            raise ValueError

    def order_by(self, column, ordering='asc'):
        index = self.headers.index(column)
        if ordering.lower().startswith('desc'):
            sort_function = lambda x, y: cmp(y[index], x[index])
        else:
            sort_function = lambda x, y: cmp(x[index], y[index])
        self._rows.sort(sort_function)

    def encode(self, codec=None):
        if codec is None:
            codec = self.output_encoding
        self.headers = [_unicode_encode(x, codec) for x in self.headers]
        rows = []
        for row in self._rows:
            rows.append([_unicode_encode(value, codec) for value in row])
        self._rows = rows

    def decode(self, codec=None):
        if codec is None:
            codec = self.input_encoding
        rows = []
        for row in self._rows:
            rows.append([_str_decode(v, codec) for v in row])
        self._rows = rows
        self.headers = [_str_decode(h, codec) for h in self.headers]

    def _max_column_sizes(self):
        max_size = {}
        for column in self.headers:
            sizes = [len(unicode(value)) for value in self[column]]
            max_column_size = max(sizes + [len(column)])
            max_size[column] = max_column_size
        return max_size

    def _make_line_from_row_data(self, row_data):
        return '%s %s %s' % (self.pipe, (' %s ' % self.pipe).join(row_data),
                             self.pipe)

    def __unicode__(self):
        max_size = self._max_column_sizes()
        if not len(self.headers) and not len(self._rows):
            return unicode()

        dashes = []
        centered_headers = []
        for header in self.headers:
            centered_headers.append(header.center(max_size[header]))
            dashes.append(self.dash * (max_size[header] + 2))
        split_line = self.plus + self.plus.join(dashes) + self.plus
        header_line = self._make_line_from_row_data(centered_headers)

        result = [split_line, header_line, split_line]
        for row in self._rows:
            row_data = []
            for i, info in enumerate(row):
                data = unicode(info).rjust(max_size[self.headers[i]])
                row_data.append(data)
            result.append(self._make_line_from_row_data(row_data))
        if self._rows:
            result.append(split_line)
        return '\n'.join(result)

    def __str__(self):
        return self.__unicode__().encode(self.output_encoding)

    def to_list_of_dicts(self, encoding=''):
        if encoding is not None:
            self.encode(encoding or self.output_encoding)
        rows = [dict(zip(self.headers, row)) for row in self._rows]
        if encoding is not None:
            self.decode(encoding or self.output_encoding)
        return rows

    def _identify_type_of_data(self):
        """Create `self.types`, a `dict` in which each key is a table header
        (from `self.headers`) and value is a type in:
        `(int, float, datetime.date, datetime.datetime, str)`.

        The types are identified trying to convert each column value to each
        type.
        """
        date_regex = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
        datetime_regex = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2} '
                                    '[0-9]{2}:[0-9]{2}:[0-9]{2}$')
        for header in self.headers:
            column = self[header]
            possible_types = Counter()
            for value in column:
                if value is None or value == '':
                    continue # None and empty string don't affect type
                possible_types[str] += 1
                try:
                    int_value = int(value)
                    if unicode(int_value) == unicode(value):
                        possible_types[int] += 1
                except ValueError:
                    pass
                try:
                    float_value = float(value)
                    possible_types[float] += 1
                except ValueError:
                    pass
                if datetime_regex.match(unicode(value)):
                    possible_types[datetime.datetime] += 1
                if date_regex.match(unicode(value)):
                    possible_types[datetime.date] += 1
            str_count = possible_types[str]
            types = [float, int, datetime.datetime, datetime.date]
            result = [type_ for type_ in types
                            if type_ in possible_types and \
                               possible_types[type_] == str_count]
            if not len(result):
                type_ = str
            else:
                type_ = result[-1]
            self.types[header] = type_

    def normalize_types(self):
        self._identify_type_of_data()
        rows_converted = []
        for row in self._rows:
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
        self._rows = rows_converted

    def to_dict(self, only=None, key=None, value=None):
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
            for row in self._rows:
                table_dict[row[key_index]] = row[value_index]
        else:
            for index, column in enumerate(zip(*self._rows)):
                header_name = self.headers[index]
                if only is None or header_name in only:
                    table_dict[header_name] = list(column)
        self.decode(self.output_encoding)
        return table_dict

    def _load_plugin(self, plugin_name):
        if plugin_name not in self.plugins:
            complete_name = 'outputty.plugin_' + plugin_name
            plugin = __import__(complete_name, fromlist=['outputty'])
            self.plugins[plugin_name] = plugin
        return self.plugins[plugin_name]

    def read(self, plugin_name, *args, **kwargs):
        plugin = self._load_plugin(plugin_name)
        return plugin.read(self, *args, **kwargs)

    def write(self, plugin_name, *args, **kwargs):
        plugin = self._load_plugin(plugin_name)
        return plugin.write(self, *args, **kwargs)

    def append(self, item):
        item = self._prepare_to_append(item)
        self._rows.append(item)

    def _prepare_to_append(self, item):
        if isinstance(item, dict):
            row = []
            for column in self.headers:
                if column in item:
                    value = item[column]
                else:
                    value = None
                row.append(value)
        elif isinstance(item, (tuple, set)):
            row = list(item)
        elif isinstance(item, list):
            row = item
        else:
            raise ValueError
        if len(row) != len(self.headers):
            raise ValueError
        return [_str_decode(value, self.input_encoding) for value in row]

    def extend(self, items):
        """Append a lot of items.
        `items` should be a list of new rows, each row can be represented as
        `list`, `tuple` or `dict`.
        If one of the rows causes a `ValueError` (for example, because it has
        more or less elements than it should), then nothing will be appended to
        `Table`.
        """
        new_items = []
        for item in items:
            new_items.append(self._prepare_to_append(item))
        for item in new_items:
            self.append(item)

    def __len__(self):
        """Returns the number of rows. Same as `len(list)`."""
        return len(self._rows)

    def count(self, row):
        """Returns how many rows are equal to `row` in `Table`.
        Same as `list.count`.
        """
        return self._rows.count(self._prepare_to_append(row))

    def index(self, x, i=None, j=None):
        """Returns the index of row `x` in table (starting from zero).
        Same as `list.index`.
        """
        x = self._prepare_to_append(x)
        if i is None and j is None:
            return self._rows.index(x)
        elif j is None:
            return self._rows.index(x, i)
        else:
            return self._rows.index(x, i, j)

    def insert(self, index, row):
        """Insert `row` in the position `index` on `Table`.
        Same as `list.insert`.
        `row` can be `list`, `tuple` or `dict`.
        """
        self._rows.insert(index, self._prepare_to_append(row))

    def pop(self, index=-1):
        """Removes and returns row in position `index` on `Table`. `index`
        defaults to -1.
        Same as `list.pop`.
        """
        return self._rows.pop(index)

    def remove(self, row):
        """Removes first occurrence of `row` on `Table`.
        Raises `ValueError` if `row` is not found.
        Same as `list.remove`.
        """
        self._rows.remove(self._prepare_to_append(row))

    def reverse(self):
        """Reverse the order of rows *in place* (does not return a new `Table`,
        change the rows in this instance of `Table`).
        Same as `list.reverse`.
        """
        self._rows.reverse()

    def append_column(self, name, values, position=None, row_as_dict=False):
        """Append a column in the end of table"""
        if (type(values) != types.FunctionType and \
            len(values) != len(self)) or \
           name in self.headers:
            raise ValueError
        if position is None:
            insert_header = lambda name: self.headers.append(name)
            insert_data = lambda row, value: row.append(value)
        else:
            insert_header = lambda name: self.headers.insert(position, name)
            insert_data = lambda row, value: row.insert(position, value)
        for index, row in enumerate(self):
            if type(values) == types.FunctionType:
                if row_as_dict:
                    value = values({header: row[index] \
                                    for index, header in \
                                        enumerate(self.headers)})
                else:
                    value = values(row)
            else:
                value = values[index]
            insert_data(row, _str_decode(value, self.input_encoding))
        insert_header(name)
