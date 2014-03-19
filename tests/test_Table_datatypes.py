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

import datetime
import unittest

from outputty import date_regex, datetime_regex, Table


class TestTableDataTypes(unittest.TestCase):
    def test_should_indentify_type_str_when_only_headers_present(self):
        table = Table(headers=['eggs', 'ham'])
        table._identify_data_types()
        self.assertEqual(table.types['eggs'], str)
        self.assertEqual(table.types['ham'], str)

    def test_should_indentify_type_str_correctly(self):
        table = Table(headers=['eggs', 'ham'], input_encoding='iso-8859-1')
        table.append(['spam eggs', 1])
        table.append(['spam spam', 3.14])
        table.append(['eggs spam', 'testing'])
        table.append(['spam spam', '2011-11-23'])
        table.append(['spam  ham', '2011-11-23 02:00:17'])
        table.append([u'álvaro'.encode('iso-8859-1'), '2011-11-23 02:00:17'])
        table._identify_data_types()
        self.assertEqual(table.types['eggs'], str)
        self.assertEqual(table.types['ham'], str)

    def test_should_indentify_type_int_correctly(self):
        table = Table(headers=['spam'])
        table.append([1])
        table.append([2])
        table._identify_data_types()
        self.assertEqual(table.types['spam'], int)

    def test_should_not_indentify_non_fractional_floats_as_int(self):
        table = Table(headers=['ham'])
        table.append([1.0])
        table.append([2.0])
        table.append([3.0])
        table._identify_data_types()
        self.assertEqual(table.types['ham'], float)

    def test_should_indentify_type_float_correctly(self):
        table = Table(headers=['ham'])
        table.append(["3"])
        table.append(["3.14"])
        table.append([""])
        table.append(["2.71"])
        table._identify_data_types()
        self.assertEqual(table.types['ham'], float)

    def test_should_indentify_type_date_correctly(self):
        table = Table(headers=['Python'])
        table.append(['2010-11-15'])
        table.append(['2011-11-20'])
        table._identify_data_types()
        self.assertEqual(table.types['Python'], datetime.date)

    def test_should_indentify_type_datetime_correctly(self):
        table = Table(headers=['Monty'])
        table.append(['2010-11-15 02:42:01'])
        table.append(['2011-11-20 21:05:59'])
        table._identify_data_types()
        self.assertEqual(table.types['Monty'], datetime.datetime)

    def test_None_should_not_affect_data_type(self):
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python'])
        table.append([1, 2.71, '2011-01-01', '2011-01-01 00:00:00', 'asd'])
        table.append([None, None, None, None, None])
        table._identify_data_types()
        self.assertEquals(table.types['spam'], int)
        self.assertEquals(table.types['eggs'], float)
        self.assertEquals(table.types['ham'], datetime.date)
        self.assertEquals(table.types['Monty'], datetime.datetime)
        self.assertEquals(table.types['Python'], str)

    def test_empty_string_should_not_affect_data_type(self):
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python'])
        table.append([1, 2.71, '2011-01-01', '2011-01-01 00:00:00', 'asd'])
        table.append(['', '', '', '', ''])
        table._identify_data_types()
        self.assertEquals(table.types['spam'], int)
        self.assertEquals(table.types['eggs'], float)
        self.assertEquals(table.types['ham'], datetime.date)
        self.assertEquals(table.types['Monty'], datetime.datetime)
        self.assertEquals(table.types['Python'], str)

    def test_normalize_types_should_convert_types_correctly(self):
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python',
                               'rules', 'rocks'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 'T'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 'F'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 't'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 'f'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 'true'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 'false'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 'True'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 'False'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 'y'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 'n'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 'Y'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
            '', 'N'])
        table.append([None, None, None, None, None, '', 1])
        table.append([None, None, None, None, 42, '', 0])
        table.append([None, None, None, None, None, '', ''])
        table.normalize_types()
        self.assertEqual(table[0][0], 1)
        self.assertEqual(table[0][1], 2.71)
        self.assertEqual(table[0][2], datetime.date(2011, 1, 1))
        self.assertEqual(table[0][3],
                          datetime.datetime(2011, 1, 1, 2, 3, 4))
        self.assertEqual(table[0][4], 'asd')
        self.assertEqual(table.types['rules'], str)
        self.assertEqual(table.types['rocks'], bool)

        expected_bools = [True, False, True, False, True, False, True, False,
                True, False, True, False, True, False, None]
        self.assertEqual(table['rocks'], expected_bools)

    def test_identify_data_types_with_normalized_types_should_not_affect(self):
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python'])
        table.append([
            1,
            2.71,
            datetime.date(2011, 01, 01),
            datetime.datetime(2011, 01, 01, 0, 0, 0),
            'asd'])
        table.normalize_types()
        table._identify_data_types()
        self.assertEquals(table.types['spam'], int)
        self.assertEquals(table.types['eggs'], float)
        self.assertEquals(table.types['ham'], datetime.date)
        self.assertEquals(table.types['Monty'], datetime.datetime)
        self.assertEquals(table.types['Python'], str)

    def test_should_be_able_to_change_converters(self):

        def convert_to_bool(value, encoding):
            possible_values = ('t', 'f', 'true', 'false', '0', '1', 'y', 'n')
            if unicode(value).lower() in possible_values:
                return 'bool={}'.format(value)
            else:
                raise ValueError("Can't be bool")

        def convert_to_int(value, encoding):
            converted = int(value)
            if str(converted) != str(value):
                raise ValueError('It is a float')
            else:
                return 'int={}'.format(converted)

        def convert_to_float(value, encoding):
            converted = float(value)
            return 'float={}'.format(converted)

        def convert_to_datetime(value, input_encoding):
            if datetime_regex.match(unicode(value)) is None:
                raise ValueError("Can't be datetime")
            else:
                return 'datetime={}'.format(value)

        def convert_to_date(value, input_encoding):
            if date_regex.match(unicode(value)) is None:
                raise ValueError("Can't be date")
            else:
                return 'date={}'.format(value)

        def convert_to_str(value, input_encoding):
            if not isinstance(value, unicode):
                if not isinstance(value, str):
                    value = str(value)
                value = value.decode(input_encoding)
            return 'str[{}]'.format(len(value))

        converters = {
                int: convert_to_int,
                float: convert_to_float,
                bool: convert_to_bool,
                datetime.date: convert_to_date,
                datetime.datetime: convert_to_datetime,
                str: convert_to_str,}
        headers = ['spam', 'eggs', 'ham', 'Monty', 'Python', 'rules']
        table = Table(headers=headers, converters=converters)
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', 'asd',
                'True'])
        table.normalize_types()
        self.assertEqual(table[0][0], 'int=1')
        self.assertEqual(table[0][1], 'float=2.71')
        self.assertEqual(table[0][2], 'date=2011-01-01')
        self.assertEqual(table[0][3], 'datetime=2011-01-01 02:03:04')
        self.assertEqual(table[0][4], 'str[3]')
        self.assertEqual(table[0][5], 'bool=True')

    def test_should_be_able_to_specify_converter_sample(self):
        headers = ['spam', 'eggs', 'ham', 'Monty', 'Python']
        table = Table(headers=headers, converter_sample=3)
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', ''])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', ''])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04', ''])
        table.append(['-', '-', '-', '-', 123])
        table.append(['-', '-', '-', '-', ''])
        table.append(['-', '-', '-', '-', ''])
        table._identify_data_types()
        expected_types = {
                'spam': int,
                'eggs': float,
                'ham': datetime.date,
                'Monty': datetime.datetime,
                'Python': str,}
        self.assertEqual(table.types, expected_types)

    # TODO: add data type checkers AND converters. data type checkers should
    # receive a set of the entire column
