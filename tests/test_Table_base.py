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

from textwrap import dedent
import unittest
from outputty import Table


class TestTable(unittest.TestCase):
    def test_table_with_only_one_header_without_data(self):
        my_table = Table(headers=['test'])
        self.assertEqual(str(my_table), dedent('''
        +------+
        | test |
        +------+
        ''').strip())
        my_table = Table(headers=['blabla'])
        self.assertEqual(str(my_table), dedent('''
        +--------+
        | blabla |
        +--------+
        ''').strip())

    def test_table_with_many_headers_without_data(self):
        my_table = Table(headers=['spam', 'ham'])
        self.assertEqual(str(my_table), dedent('''
        +------+-----+
        | spam | ham |
        +------+-----+
        ''').strip())
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        ''').strip())

    def test_table_with_many_headers_and_one_row_same_size(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': 123, 'spam': 4567, 'eggs': 8910})
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        | 123 | 4567 | 8910 |
        +-----+------+------+
        ''').strip())

    def test_table_with_many_headers_and_rows_same_size(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': 123, 'spam': 4567, 'eggs': 8910})
        my_table.rows.append({'ham': 321, 'spam': 7654, 'eggs': 1098})
        my_table.rows.append({'ham': 'abc', 'spam': 'defg', 'eggs': 'hijk'})
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        | 123 | 4567 | 8910 |
        | 321 | 7654 | 1098 |
        | abc | defg | hijk |
        +-----+------+------+
        ''').strip())

    def test_table_with_many_headers_and_rows_missing_some_columns(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'spam': 4567, 'eggs': 8910})
        my_table.rows.append({'ham': 321, 'eggs': 1098})
        my_table.rows.append({'ham': 'abc', 'spam': 'defg'})
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        |     | 4567 | 8910 |
        | 321 |      | 1098 |
        | abc | defg |      |
        +-----+------+------+
        ''').strip())

    def test_table_with_changed_separators(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'], dash='=', pipe='-',
                         plus='*')
        my_table.rows.append({'ham': '', 'spam': '', 'eggs': ''})
        my_table.rows.append({'ham': 1, 'spam': 2, 'eggs': 3})
        my_table.rows.append({'ham': 11, 'spam': 22, 'eggs': 33})
        self.assertEqual(str(my_table), dedent('''\
        *=====*======*======*
        - ham - spam - eggs -
        *=====*======*======*
        -     -      -      -
        -   1 -    2 -    3 -
        -  11 -   22 -   33 -
        *=====*======*======*'''))

    def test_table_should_accept_rows_as_dict_list_tuple_int_or_float(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': 'eggs', 'spam': 'ham', 'eggs': 'spam'})
        my_table.rows.append([1, 42, 3])
        my_table.rows.append([3.14, 2.71, 0.0])
        my_table.rows.append(('spam', 'eggs', 'ham'))
        self.assertEqual(str(my_table), dedent('''
        +------+------+------+
        | ham  | spam | eggs |
        +------+------+------+
        | eggs |  ham | spam |
        |    1 |   42 |    3 |
        | 3.14 | 2.71 |  0.0 |
        | spam | eggs |  ham |
        +------+------+------+
        ''').strip())

    def test_table_should_accept_headers_as_dict_list_tuple_int_or_float(self):
        my_table = Table(headers=[42, 3.14, (4, 2), [3, 14], {'answer': 42}])
        self.assertEqual(str(my_table), dedent('''
        +----+------+--------+---------+----------------+
        | 42 | 3.14 | (4, 2) | [3, 14] | {'answer': 42} |
        +----+------+--------+---------+----------------+
        ''').strip())

    def test_table_with_many_headers_and_rows_right_aligned(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': '', 'spam': '', 'eggs': ''})
        my_table.rows.append({'ham': 1, 'spam': 2, 'eggs': 3})
        my_table.rows.append({'ham': 11, 'spam': 22, 'eggs': 33})
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        |     |      |      |
        |   1 |    2 |    3 |
        |  11 |   22 |   33 |
        +-----+------+------+
        ''').strip())

    def test_table_with_headers_little_than_rows(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': 'ham spam ham', 'spam': 'spam eggs spam',
                              'eggs': 'eggs ham eggs'})
        self.assertEqual(str(my_table), dedent('''
        +--------------+----------------+---------------+
        |     ham      |      spam      |      eggs     |
        +--------------+----------------+---------------+
        | ham spam ham | spam eggs spam | eggs ham eggs |
        +--------------+----------------+---------------+
        ''').strip())

    def test_character_count_in_row_data_should_use_unicode(self):
        my_table = Table(headers=['First name', 'Last name'])
        my_table.rows.append({'First name': 'Álvaro', 'Last name': 'Justen'})
        my_table.rows.append(['Tatiana', 'Al-Chueyr'])
        my_table.rows.append(('Flávio', 'Amieiro'))
        self.assertEqual(str(my_table), dedent('''
        +------------+-----------+
        | First name | Last name |
        +------------+-----------+
        |     Álvaro |    Justen |
        |    Tatiana | Al-Chueyr |
        |     Flávio |   Amieiro |
        +------------+-----------+
        ''').strip())

    def test_character_count_in_headers_should_be_unicode(self):
        my_table = Table(headers=['ÁÀÃÂÇ', 'ÇÉÈẼÊ'])
        my_table.rows.append(('spam', 'eggs'))
        my_table.rows.append(('eggs', 'spam'))
        self.assertEqual(str(my_table), dedent('''
        +-------+-------+
        | ÁÀÃÂÇ | ÇÉÈẼÊ |
        +-------+-------+
        |  spam |  eggs |
        |  eggs |  spam |
        +-------+-------+
        ''').strip())

    def test_input_and_ouput_character_encoding_in_headers(self):
        my_table = Table(headers=['Álvaro'.decode('utf8').encode('utf16')],
                         input_encoding='utf16', output_encoding='iso-8859-1')
        self.assertEqual(str(my_table), dedent('''
        +--------+
        | Álvaro |
        +--------+
        ''').strip().decode('utf8').encode('iso-8859-1'))

    def test_output_character_encoding_in_method___str__(self):
        my_table = Table(headers=['Álvaro'.decode('utf8').encode('utf16')],
                         input_encoding='utf16', output_encoding='iso-8859-1')
        my_table.rows.append(['Píton'.decode('utf8').encode('utf16')])

        output = dedent('''
        +--------+
        | Álvaro |
        +--------+
        |  Píton |
        +--------+
        ''').strip().decode('utf8').encode('iso-8859-1')
        self.assertEqual(str(my_table), output)

    def test___unicode__should_return_unicode_no_matter_the_input_encoding(self):
        my_table = Table(headers=['ÁÀÃÂÇ', 'ÇÉÈẼÊ'])
        my_table.rows.append(('spam', 'eggs'))
        my_table.rows.append(('eggs', 'spam'))
        self.assertEqual(unicode(my_table), dedent('''
        +-------+-------+
        | ÁÀÃÂÇ | ÇÉÈẼÊ |
        +-------+-------+
        |  spam |  eggs |
        |  eggs |  spam |
        +-------+-------+
        ''').strip().decode('utf8'))

    def test_headers_of_one_table_should_not_affect_other(self):
        table_1 = Table()
        table_1.headers.append('spam')
        table_1.headers.append('eggs')
        table_2 = Table()

        self.assertEquals(len(table_1.headers), 2)
        self.assertEquals(len(table_2.headers), 0)

    def test_to_dict_should_return_a_list_of_dict_with_headers_as_keys(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append((123, 456, 789))
        my_table.rows.append({'ham': 'abc', 'spam': 'def', 'eggs': 'ghi'})
        my_table.rows.append((987, 654, 321))
        my_dict = my_table.to_list_of_dicts()
        self.assertEquals(len(my_dict), 3)
        self.assertEquals(my_dict[0]['ham'], 123)
        self.assertEquals(my_dict[0]['spam'], 456)
        self.assertEquals(my_dict[0]['eggs'], 789)
        self.assertEquals(my_dict[1]['ham'], 'abc')
        self.assertEquals(my_dict[1]['spam'], 'def')
        self.assertEquals(my_dict[1]['eggs'], 'ghi')
        self.assertEquals(my_dict[2]['ham'], 987)
        self.assertEquals(my_dict[2]['spam'], 654)
        self.assertEquals(my_dict[2]['eggs'], 321)
