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

import unittest
import datetime
from outputty import Table


class TestTableDataTypes(unittest.TestCase):
    def test_should_indentify_type_str_when_only_headers_present(self):
        table = Table(headers=['eggs', 'ham'])
        table._identify_type_of_data()
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
        table._identify_type_of_data()
        self.assertEqual(table.types['eggs'], str)
        self.assertEqual(table.types['ham'], str)

    def test_should_indentify_type_int_correctly(self):
        table = Table(headers=['spam'])
        table.append([1])
        table.append([2])
        table._identify_type_of_data()
        self.assertEqual(table.types['spam'], int)

    def test_should_not_indentify_non_fractional_floats_as_int(self):
        table = Table(headers=['ham'])
        table.append([1.0])
        table.append([2.0])
        table.append([3.0])
        table._identify_type_of_data()
        self.assertEqual(table.types['ham'], float)

    def test_should_indentify_type_float_correctly(self):
        table = Table(headers=['ham'])
        table.append(["3"])
        table.append(["3.14"])
        table.append([""])
        table.append(["2.71"])
        table._identify_type_of_data()
        self.assertEqual(table.types['ham'], float)

    def test_should_indentify_type_date_correctly(self):
        table = Table(headers=['Python'])
        table.append(['2010-11-15'])
        table.append(['2011-11-20'])
        table._identify_type_of_data()
        self.assertEqual(table.types['Python'], datetime.date)

    def test_should_indentify_type_datetime_correctly(self):
        table = Table(headers=['Monty'])
        table.append(['2010-11-15 02:42:01'])
        table.append(['2011-11-20 21:05:59'])
        table._identify_type_of_data()
        self.assertEqual(table.types['Monty'], datetime.datetime)

    def test_None_should_not_affect_data_type(self):
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python'])
        table.append([1, 2.71, '2011-01-01', '2011-01-01 00:00:00', 'asd'])
        table.append([None, None, None, None, None])
        table._identify_type_of_data()
        self.assertEquals(table.types['spam'], int)
        self.assertEquals(table.types['eggs'], float)
        self.assertEquals(table.types['ham'], datetime.date)
        self.assertEquals(table.types['Monty'], datetime.datetime)
        self.assertEquals(table.types['Python'], str)

    def test_empty_string_should_not_affect_data_type(self):
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python'])
        table.append([1, 2.71, '2011-01-01', '2011-01-01 00:00:00', 'asd'])
        table.append(['', '', '', '', ''])
        table._identify_type_of_data()
        self.assertEquals(table.types['spam'], int)
        self.assertEquals(table.types['eggs'], float)
        self.assertEquals(table.types['ham'], datetime.date)
        self.assertEquals(table.types['Monty'], datetime.datetime)
        self.assertEquals(table.types['Python'], str)

    def test_normalize_types_should_convert_types_correctly(self):
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python'])
        table.append(['1', '2.71', '2011-01-01', '2011-01-01 02:03:04',
                           'asd'])
        table.append([None, None, None, None, None])
        table.append([None, None, None, None, 42])
        table.normalize_types()
        self.assertEquals(table[0][0], 1)
        self.assertEquals(table[0][1], 2.71)
        self.assertEquals(table[0][2], datetime.date(2011, 1, 1))
        self.assertEquals(table[0][3],
                          datetime.datetime(2011, 1, 1, 2, 3, 4))
        self.assertEquals(table[0][4], 'asd')

    def test_running_identify_data_type_with_normalized_types_should_return_correct_results(self):
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python'])
        table.append([1, 2.71, '2011-01-01', '2011-01-01 00:00:00', 'asd'])
        table.append(['', '', '', '', ''])
        table.normalize_types()
        table._identify_type_of_data()
        self.assertEquals(table.types['spam'], int)
        self.assertEquals(table.types['eggs'], float)
        self.assertEquals(table.types['ham'], datetime.date)
        self.assertEquals(table.types['Monty'], datetime.datetime)
        self.assertEquals(table.types['Python'], str)

