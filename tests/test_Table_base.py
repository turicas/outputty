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
        my_table.append({'ham': 123, 'spam': 4567, 'eggs': 8910})
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        | 123 | 4567 | 8910 |
        +-----+------+------+
        ''').strip())

    def test_table_with_many_headers_and_rows_same_size(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.append({'ham': 123, 'spam': 4567, 'eggs': 8910})
        my_table.append({'ham': 321, 'spam': 7654, 'eggs': 1098})
        my_table.append({'ham': 'abc', 'spam': 'defg', 'eggs': 'hijk'})
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
        my_table.append({'spam': 4567, 'eggs': 8910})
        my_table.append({'ham': 321, 'eggs': 1098})
        my_table.append({'ham': 'abc', 'spam': 'defg'})
        self.assertEqual(str(my_table), dedent('''
        +------+------+------+
        | ham  | spam | eggs |
        +------+------+------+
        | None | 4567 | 8910 |
        |  321 | None | 1098 |
        |  abc | defg | None |
        +------+------+------+
        ''').strip())

    def test_table_with_changed_separators(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'], dash='=', pipe='-',
                         plus='*')
        my_table.append({'ham': '', 'spam': '', 'eggs': ''})
        my_table.append({'ham': 1, 'spam': 2, 'eggs': 3})
        my_table.append({'ham': 11, 'spam': 22, 'eggs': 33})
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
        my_table.append({'ham': 'eggs', 'spam': 'ham', 'eggs': 'spam'})
        my_table.append([1, 42, 3])
        my_table.append([3.14, 2.71, 0.0])
        my_table.append(('spam', 'eggs', 'ham'))
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

    def test_table_headers_should_accept_only_strings(self):
        with self.assertRaises(ValueError):
            my_table = Table(headers=[42, 3.14, (4, 2), [3, 14],
                                      {'answer': 42}, None])

    def test_table_headers_should_be_unique(self):
        with self.assertRaises(ValueError):
            my_table = Table(headers=['a', 'a'])

    def test_None_in_rows(self):
        my_table = Table(headers=['a', 'b', 'c'])
        my_table.append([None, None, None])
        self.assertEqual(str(my_table), dedent('''
        +------+------+------+
        |  a   |  b   |  c   |
        +------+------+------+
        | None | None | None |
        +------+------+------+
        ''').strip())

    def test_table_with_many_headers_and_rows_right_aligned(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.append({'ham': '', 'spam': '', 'eggs': ''})
        my_table.append({'ham': 1, 'spam': 2, 'eggs': 3})
        my_table.append({'ham': 11, 'spam': 22, 'eggs': 33})
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
        my_table.append({'ham': 'ham spam ham', 'spam': 'spam eggs spam',
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
        my_table.append({'First name': 'Álvaro', 'Last name': 'Justen'})
        my_table.append(('Flávio', 'Amieiro'))
        self.assertEqual(str(my_table), dedent('''
        +------------+-----------+
        | First name | Last name |
        +------------+-----------+
        |     Álvaro |    Justen |
        |     Flávio |   Amieiro |
        +------------+-----------+
        ''').strip())

    def test_character_count_in_headers_should_be_unicode(self):
        my_table = Table(headers=['ÁÀÃÂÇ', 'ÇÉÈẼÊ'])
        my_table.append(('spam', 'eggs'))
        my_table.append(('eggs', 'spam'))
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
        my_table.append(['Píton'.decode('utf8').encode('utf16')])

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
        my_table.append(('spam', 'eggs'))
        my_table.append(('eggs', 'spam'))
        self.assertEqual(unicode(my_table), dedent('''
        +-------+-------+
        | ÁÀÃÂÇ | ÇÉÈẼÊ |
        +-------+-------+
        |  spam |  eggs |
        |  eggs |  spam |
        +-------+-------+
        ''').strip().decode('utf8'))

    def test_should_accept_None_in_rows(self):
        my_table = Table(headers=['spam'])
        my_table.append([None])
        self.assertEqual(unicode(my_table), dedent('''
        +------+
        | spam |
        +------+
        | None |
        +------+
        ''').strip())

    def test_headers_of_one_table_should_not_affect_other(self):
        table_1 = Table()
        table_1.headers.append('spam')
        table_1.headers.append('eggs')
        table_2 = Table()

        self.assertEquals(len(table_1.headers), 2)
        self.assertEquals(len(table_2.headers), 0)

    def test_decode_method_should_normalize_and_use_input_encoding(self):
        my_table = Table(headers=[u'ham'.encode('utf16'),
                                  u'spam'.encode('utf16'),
                                  u'eggs'.encode('utf16')],
                         input_encoding='utf16')
        my_table.append((123, 456, 789))
        my_table.append((987, 654, u'python'.encode('utf16')))
        my_table.decode()
        my_table.encode()
        self.assertEquals(my_table[1][2], u'python')

    def test_encode_method_should_normalize_and_use_output_encoding(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'],
                         output_encoding='utf16')
        my_table.append((123, 456, 789))
        my_table.append({'ham': 'abc', 'spam': 'def', 'eggs': 'ghi'})
        my_table.append((987, 654, 'python'))
        my_table.decode()
        my_table.encode()
        self.assertEquals(my_table[1][0], u'abc'.encode('utf16'))
        self.assertEquals(my_table[1][1], u'def'.encode('utf16'))
        self.assertEquals(my_table[1][2], u'ghi'.encode('utf16'))
        self.assertEquals(my_table[2][2], u'python'.encode('utf16'))

    def test_to_dict_should_return_a_list_of_dict_with_headers_as_keys(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.append((123, 456, 789))
        my_table.append({'ham': 'abc', 'spam': 'def', 'eggs': 'ghi'})
        my_table.append((987, 654, 321))
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

    def test_to_dict_should_return_unicode_data_when_encoding_is_None(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.append({'ham': 'á', 'spam': 'ç', 'eggs': 'à'})
        my_dict = my_table.to_list_of_dicts(encoding=None)
        self.assertEquals(len(my_dict), 1)
        self.assertTrue(isinstance(my_dict[0]['ham'], unicode))
        self.assertTrue(isinstance(my_dict[0]['spam'], unicode))
        self.assertTrue(isinstance(my_dict[0]['eggs'], unicode))
        self.assertEquals(my_dict[0]['ham'], u'á')
        self.assertEquals(my_dict[0]['spam'], u'ç')
        self.assertEquals(my_dict[0]['eggs'], u'à')
        my_table = Table(headers=['ham', 'spam', 'eggs'],
                         output_encoding='utf16')
        my_table.append({'ham': 'á', 'spam': 'ç', 'eggs': 'à'})
        my_dict = my_table.to_list_of_dicts(encoding='iso-8859-1')
        self.assertEquals(len(my_dict), 1)
        self.assertEquals(my_dict[0]['ham'], u'á'.encode('iso-8859-1'))
        self.assertEquals(my_dict[0]['spam'], u'ç'.encode('iso-8859-1'))
        self.assertEquals(my_dict[0]['eggs'], u'à'.encode('iso-8859-1'))

    def test_list_of_dicts_should_handle_output_encoding_correctly(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'],
                         output_encoding='utf16')
        my_table.append((123, 456, 789))
        my_table.append({'ham': 'abc', 'spam': 'def', 'eggs': 'ghi'})
        my_table.append((987, 654, 321))
        my_dicts = my_table.to_list_of_dicts()
        self.assertEquals(len(my_dicts), 3)
        self.assertEquals(my_dicts[1][u'ham'.encode('utf16')],
                          u'abc'.encode('utf16'))
        self.assertEquals(my_dicts[1][u'spam'.encode('utf16')],
                          u'def'.encode('utf16'))
        self.assertEquals(my_dicts[1][u'eggs'.encode('utf16')],
                          u'ghi'.encode('utf16'))
        self.assertEquals(my_dicts[2][u'ham'.encode('utf16')], 987)
        self.assertEquals(my_dicts[2][u'spam'.encode('utf16')], 654)
        self.assertEquals(my_dicts[2][u'eggs'.encode('utf16')], 321)

    def test_ordering_table_with_one_column(self):
        my_table = Table(headers=['spam'])
        my_table.append(['ham'])
        my_table.append(['eggs'])
        my_table.append(['idle'])
        my_table.order_by('spam')
        output = dedent('''
        +------+
        | spam |
        +------+
        | eggs |
        |  ham |
        | idle |
        +------+
        ''').strip()
        self.assertEqual(str(my_table), output)

    def test_ordering_two_columns_table_by_second_header(self):
        my_table = Table(headers=['spam', 'ham'])
        my_table.append(('eggs', 'ham'))
        my_table.append(('ham', 'eggs'))
        my_table.append(('ham', '123'))
        my_table.order_by('ham')
        output = dedent('''
        +------+------+
        | spam | ham  |
        +------+------+
        |  ham |  123 |
        |  ham | eggs |
        | eggs |  ham |
        +------+------+
        ''').strip()
        self.assertEqual(str(my_table), output)

    def test_ordering_table_with_missing_column_in_some_rows(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.append({'spam': 'Eric', 'eggs': 'Idle'})
        my_table.append({'ham': 'John', 'eggs': 'Cleese'})
        my_table.append({'ham': 'Terry', 'spam': 'Jones'})
        my_table.order_by('spam')
        self.assertEqual(str(my_table), dedent('''
        +-------+-------+--------+
        |  ham  |  spam |  eggs  |
        +-------+-------+--------+
        |  John |  None | Cleese |
        |  None |  Eric |   Idle |
        | Terry | Jones |   None |
        +-------+-------+--------+
        ''').strip())

    def test_ordering_table_with_rows_as_dict_list_tuple(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.append({'ham': 'eggs', 'spam': 'ham', 'eggs': 'spam'})
        my_table.append({'ham': 'eggs', 'spam': 'python', 'eggs': 'spam'})
        my_table.append([1, 42, 3])
        my_table.append([3.14, 2.71, 0.0])
        my_table.append(('spam', 'eggs', 'ham'))
        my_table.order_by('spam')
        self.assertEqual(str(my_table), dedent('''
        +------+--------+------+
        | ham  |  spam  | eggs |
        +------+--------+------+
        | 3.14 |   2.71 |  0.0 |
        |    1 |     42 |    3 |
        | spam |   eggs |  ham |
        | eggs |    ham | spam |
        | eggs | python | spam |
        +------+--------+------+
        ''').strip())

    def test_ordering_table_without_data(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.order_by('spam')
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        ''').strip())

    def test_ordering_numbers(self):
        my_table = Table(headers=['spam'])
        my_table.append([5])
        my_table.append([42])
        my_table.append([3.14])
        my_table.order_by('spam')
        self.assertEqual(str(my_table), dedent('''
        +------+
        | spam |
        +------+
        | 3.14 |
        |    5 |
        |   42 |
        +------+
        ''').strip())

    def test_ordering_numbers_as_strings(self):
        my_table = Table(headers=['spam'])
        my_table.append(['5'])
        my_table.append([31])
        my_table.append(['42'])
        my_table.order_by('spam')
        self.assertEqual(str(my_table), dedent('''
        +------+
        | spam |
        +------+
        |   31 |
        |   42 |
        |    5 |
        +------+
        ''').strip())

    def test_ordering_unicode(self):
        my_table = Table(headers=['spam'])
        my_table.append(['á'])
        my_table.append(['Á'])
        my_table.order_by('spam')
        self.assertEqual(str(my_table), dedent('''
        +------+
        | spam |
        +------+
        |    Á |
        |    á |
        +------+
        ''').strip())

    def test_ordering_descending(self):
        table = Table(headers=['spam'])
        table.extend([[5], [3], [7], [10]])
        table.order_by('spam', 'descending')
        table_2 = Table(headers=['spam'])
        table_2.extend([[5], [3], [7], [10]])
        table_2.order_by('spam', 'desc')
        table_3 = Table(headers=['spam'])
        table_3.extend([[5], [3], [7], [10]])
        table_3.order_by('spam', 'DESCENDING')
        table_4 = Table(headers=['spam'])
        table_4.extend([[5], [3], [7], [10]])
        table_4.order_by('spam', 'DESC')
        expected_output = dedent('''
        +------+
        | spam |
        +------+
        |   10 |
        |    7 |
        |    5 |
        |    3 |
        +------+
        ''').strip()
        self.assertEqual(str(table), expected_output)
        self.assertEqual(str(table_2), expected_output)
        self.assertEqual(str(table_3), expected_output)
        self.assertEqual(str(table_4), expected_output)

    def test_ordering_ascending(self):
        table = Table(headers=['spam'])
        table.extend([[5], [3], [7], [10]])
        table.order_by('spam', 'ascending')
        table_2 = Table(headers=['spam'])
        table_2.extend([[5], [3], [7], [10]])
        table_2.order_by('spam', 'asc')
        table_3 = Table(headers=['spam'])
        table_3.extend([[5], [3], [7], [10]])
        table_3.order_by('spam', 'ASCENDING')
        table_4 = Table(headers=['spam'])
        table_4.extend([[5], [3], [7], [10]])
        table_4.order_by('spam', 'ASC')
        expected_output = dedent('''
        +------+
        | spam |
        +------+
        |    3 |
        |    5 |
        |    7 |
        |   10 |
        +------+
        ''').strip()
        self.assertEqual(str(table), expected_output)
        self.assertEqual(str(table_2), expected_output)

    def test_order_by_method_should_order_data_internally(self):
        my_table = Table(headers=['spam', 'ham', 'eggs'])
        my_table.append({'spam': 'Eric', 'eggs': 'Idle'})
        my_table.append({'ham': 'John', 'eggs': 'Cleese'})
        my_table.append({'ham': 'Terry', 'spam': 'Jones'})
        my_table.order_by('spam', 'asc')
        expected_output = dedent('''
        +-------+-------+--------+
        |  spam |  ham  |  eggs  |
        +-------+-------+--------+
        |  None |  John | Cleese |
        |  Eric |  None |   Idle |
        | Jones | Terry |   None |
        +-------+-------+--------+
        ''').strip()
        self.assertEqual(str(my_table), expected_output)

    def test_order_by_method_should_order_ascending_by_default(self):
        table = Table(headers=['spam'])
        table.extend([[5], [3], [7], [10]])
        table.order_by('spam')
        expected_output = dedent('''
        +------+
        | spam |
        +------+
        |    3 |
        |    5 |
        |    7 |
        |   10 |
        +------+
        ''').strip()
        self.assertEqual(str(table), expected_output)

    def test_normalize_method_should_transform_all_rows_to_lists(self):
        table = Table(headers=['spam', 'eggs', 'ham'])
        table.append(['ham', 'eggs', 'spam'])
        table.append({'ham': 42})
        table.append({'eggs': 3.14, 'spam': 2.71})
        expected = [['ham', 'eggs', 'spam'],
                    [None, None, 42],
                    [2.71, 3.14, None]]
        self.assertEqual(table[:], expected)

    def test_to_dict_should_create_a_dict_with_column_names_and_values(self):
        table = Table(headers=['spam', 'eggs'])
        table.append([42, 3.14])
        table.append(['python', 'rules'])
        table_dict = table.to_dict()
        expected = {'spam': [42, 'python'], 'eggs': [3.14, 'rules']}
        self.assertEqual(table_dict, expected)

    def test_to_dict_should_filter_some_columns(self):
        table = Table(headers=['spam', 'eggs', 'ham'])
        table.append([42, 3.14, 2.71])
        table.append(['python', 'rules', 'yeh'])
        table_dict = table.to_dict(only=('eggs', 'ham'))
        expected = {'eggs': [3.14, 'rules'], 'ham': [2.71, 'yeh']}
        self.assertEqual(table_dict, expected)

    def test_to_dict_should_filter_create_dict_from_values(self):
        table = Table(headers=['spam', 'eggs', 'ham'])
        table.append([42, 3.14, 2.71])
        table.append(['python', 'rules', 'yeh'])
        table_dict = table.to_dict(key='spam', value='ham')
        expected = {42: 2.71, 'python': 'yeh'}
        self.assertEqual(table_dict, expected)

    def test_to_dict_should_handle_encodings_correctly(self):
        table = Table(headers=['spam', 'eggs', 'ham'],
                      input_encoding='iso-8859-1', output_encoding='utf16')
        table.append([42, 3.14, 2.71])
        table.append(['python', 'rules', 'yeh'])
        table.append([u'Álvaro'.encode('iso-8859-1'), '...', 'Justen'])
        table_dict = table.to_dict(key='spam', value='ham')
        expected = {42: 2.71,
                    u'python'.encode('utf16'): u'yeh'.encode('utf16'),
                    u'Álvaro'.encode('utf16'): u'Justen'.encode('utf16')}
        self.assertEqual(table_dict, expected)

        table_dict_2 = table.to_dict()
        expected_2 = {u'spam'.encode('utf16'): [42, u'python'.encode('utf16'),
                                                u'Álvaro'.encode('utf16')],
                      u'eggs'.encode('utf16'): [3.14, u'rules'.encode('utf16'),
                                                u'...'.encode('utf16')],
                      u'ham'.encode('utf16'): [2.71, u'yeh'.encode('utf16'),
                                               u'Justen'.encode('utf16')]}
        self.assertEqual(table_dict_2, expected_2)

    def test_get_item_should_return_column_values_when_passing_string(self):
        table = Table(headers=['spam', 'eggs'])
        table.append(['python', 3.14])
        table.append(['rules', 42])
        spam_column = ['python', 'rules']
        eggs_column = [3.14, 42]
        self.assertEqual(table['spam'], spam_column)
        self.assertEqual(table['eggs'], eggs_column)

    def test_get_column_should_raises_KeyError_when_header_not_found(self):
        table = Table(headers=['spam', 'eggs'])
        with self.assertRaises(KeyError):
            table['not found column']

    def test_delete_item_passing_string_should_delete_a_entire_column(self):
        table = Table(headers=['spam', 'eggs', 'ham'])
        table.append(['python', 3.14, 1 + 5j])
        table.append(['rules', 42, 3 + 4j])
        del table['eggs']
        self.assertEquals(table.headers, ['spam', 'ham'])
        self.assertEquals(table[:], [['python', 1 + 5j], ['rules', 3 + 4j]])

    def test_table_append_should_add_a_row(self):
        table = Table(headers=['spam', 'eggs'])
        table.append(['python', 'rules'])
        table.append(['answer', 42])
        self.assertEquals(table[0], ['python', 'rules'])
        self.assertEquals(table[1], ['answer', 42])

    def test_table_append_should_convert_data_to_unicode_before(self):
        table = Table(headers=['spam', 'eggs'], input_encoding='iso-8859-1')
        table.append([u'Álvaro'.encode('iso-8859-1'), 'Justen'])
        self.assertEquals(table[0], [u'Álvaro', u'Justen'])

    def test_table_append_accept_list_tuple_and_dict_else_ValueError(self):
        table = Table(headers=['spam', 'eggs'])
        table.append(set(['eggs', 'ham']))
        table.append(('ham', 'eggs'))
        table.append({'spam': 'python', 'eggs': 'rules'})
        table.append(['answer', 42])
        table.append({'eggs': 'ham'})
        self.assertEquals(table[0], ['eggs', 'ham'])
        self.assertEquals(table[1], ['ham', 'eggs'])
        self.assertEquals(table[2], ['python', 'rules'])
        self.assertEquals(table[3], ['answer', 42])
        self.assertEquals(table[4], [None, 'ham'])
        with self.assertRaises(ValueError):
            table.append(table)

    def test_table_append_should_raises_ValueError_when_wrongly_row_size(self):
        table = Table(headers=['spam', 'eggs'])
        with self.assertRaises(ValueError):
            table.append(['answer', 42, 3.14])

    def test_table_extend(self):
        table = Table(headers=['spam', 'eggs'])
        table.extend([['python', 'rules'], ['answer', 42], {'eggs': 123}])
        self.assertEquals(table[0], ['python', 'rules'])
        self.assertEquals(table[1], ['answer', 42])
        self.assertEquals(table[2], [None, 123])

    def test_table_extend_should_add_nothing_if_an_exception_is_raised(self):
        table = Table(headers=['spam', 'eggs'])
        table.append(['hello', 'world'])
        with self.assertRaises(ValueError):
            table.extend([['python', 'rules'], ['answer', 42], [1, 2, 3]])
        self.assertEquals(table[0], ['hello', 'world'])
        self.assertEquals(len(table), 1)

    def test_table_get_item(self):
        table = Table(headers=['spam', 'eggs'])
        table.extend([['python', 'rules'], ['answer', 42]])
        self.assertEquals(table[0], ['python', 'rules'])
        self.assertEquals(table[1], ['answer', 42])

    def test_table_get_item_should_raise_IndexError_when_row_not_found(self):
        table = Table(headers=['spam', 'eggs'])
        table.extend([['python', 'rules'], ['answer', 42]])
        with self.assertRaises(IndexError):
            table[2]

    def test_table_del_item_should_work_with_rows(self):
        table = Table(headers=['spam', 'eggs'])
        table.extend([['python', 'rules'], ['answer', 42]])
        del table[0]
        self.assertEquals(table[0], ['answer', 42])

    def test_should_raises_ValueError_when_item_is_not_int_str_or_unicode(self):
        table = Table()
        with self.assertRaises(ValueError):
            table[(4, 3)]
        with self.assertRaises(ValueError):
            table[[4, 3]]
        with self.assertRaises(ValueError):
            table[{'answer': 43}]
        with self.assertRaises(ValueError):
            del table[(4, 3)]
        with self.assertRaises(ValueError):
            del table[[4, 3]]
        with self.assertRaises(ValueError):
            del table[{'answer': 43}]

    def test_len_table_should_return_len_of_rows(self):
        table = Table(headers=['spam', 'eggs'])
        table.extend([['python', 'rules'], ['answer', 42]])
        self.assertEquals(len(table), 2)

    def test_get_column_when_no_row_should_return_empty_list(self):
        table = Table(['testing'])
        self.assertEquals(table['testing'], [])

    def test_table_should_be_a_sequence(self):
        table = Table(headers=['spam', 'eggs'])
        table.extend([['python', 'rules'], ['answer', 42]])
        items = []
        for item in table:
            items.append(item)
        self.assertEquals(items[0], ['python', 'rules'])
        self.assertEquals(items[1], ['answer', 42])

    def test_get_slice(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6], [7, 8], [9, 0]])
        self.assertEquals(table[1:3], [[3, 4], [5, 6]])

    def test_del_slice(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6], [7, 8], [9, 0]])
        del table[1:3]
        self.assertEquals(table[:], [[1, 2], [7, 8], [9, 0]])

    def test_table_count(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6], [7, 8], [1, 2]])
        self.assertEquals(table.count([1, 2]), 2)

    def test_table_index(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6], [7, 8], [1, 2], [9, 0]])
        self.assertEquals(table.index([1, 2]), 0)
        self.assertEquals(table.index({'python': 1, 'rules': 2}), 0)
        self.assertEquals(table.index([5, 6]), 2)
        self.assertEquals(table.index([1, 2], 1), 4)
        with self.assertRaises(ValueError):
            non_ecxiste = table.index([1, 9])
        with self.assertRaises(ValueError):
            not_found = table.index([1, 2], 1, 3)

    def test_table_insert(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6], [7, 8], [1, 2]])
        table.insert(0, [4, 2])
        table.insert(1, {'python': 9, 'rules': 9})
        self.assertEquals(table[0], [4, 2])
        self.assertEquals(table[1], [9, 9])
        self.assertEquals(len(table), 7)

    def test_table_pop(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6]])
        self.assertEquals(table.pop(), [5, 6])
        self.assertEquals(table.pop(0), [1, 2])
        self.assertEquals(len(table), 1)

    def test_table_remove(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6], [1, 2]])
        table.remove({'python': 3, 'rules': 4})
        self.assertEquals(table[:], [[1, 2], [5, 6], [1, 2]])
        table.remove([1, 2])
        self.assertEquals(table[:], [[5, 6], [1, 2]])

    def test_table_reverse(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6]])
        table.reverse()
        self.assertEquals(table[:], [[5, 6], [3, 4], [1, 2]])

    def test_table_set_item_should_work_for_rows(self):
        table = Table(headers=['python', 'rules'])
        table.append([1, 2])
        table[0] = [4, 2]
        self.assertEquals(table[:], [[4, 2]])
        table.extend([[3, 4], [5, 6]])
        table[1:] = [[7, 8], [9, 0]]
        self.assertEquals(table[:], [[4, 2], [7, 8], [9, 0]])
        table[-3:] = [[5, 5], [7, 7], [9, 9]]
        self.assertEquals(table[:], [[5, 5], [7, 7], [9, 9]])
        with self.assertRaises(ValueError):
            table[1] = [1, 2, 3]
        with self.assertRaises(ValueError):
            table[(1, 2)] = [1, 2]

    def test_table_set_item_should_work_for_column(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6]])
        table['python'] = [2, 4, 6]
        self.assertEquals(table[:], [[2, 2], [4, 4], [6, 6]])
        with self.assertRaises(KeyError):
            should_raise_exception = table['not-found']
        with self.assertRaises(ValueError):
            table['rules'] = [1, 2, 3, 4]

    def test_table_append_column_should_change_headers_and_rows(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6]])
        table.append_column('new column', [3, 5, 7])
        self.assertEquals(table.headers, ['python', 'rules', 'new column'])
        self.assertEquals(table[:], [[1, 2, 3], [3, 4, 5], [5, 6, 7]])

    def test_table_append_column_should_work_as_item_assignment(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6]])
        table['new column'] = [3, 5, 7]
        self.assertEquals(table.headers, ['python', 'rules', 'new column'])
        self.assertEquals(table[:], [[1, 2, 3], [3, 4, 5], [5, 6, 7]])

    def test_table_append_column_should_raise_ValueError_when_wrong_size(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6]])
        with self.assertRaises(ValueError):
            table.append_column('new column', [3, 5, 7, 8])
        self.assertEquals(table.headers, ['python', 'rules'])
        self.assertEquals(table[:], [[1, 2], [3, 4], [5, 6]])

    def test_append_column_should_raise_ValueError_when_column_already_exists(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4], [5, 6]])
        with self.assertRaises(ValueError):
            table.append_column('python', [3, 5, 7])
        self.assertEquals(table.headers, ['python', 'rules'])
        self.assertEquals(table[:], [[1, 2], [3, 4], [5, 6]])

    def test_append_column_should_decode_strings(self):
        table = Table(headers=['python', 'rules'], input_encoding='iso-8859-1')
        table.extend([[1, 2], [3, 4]])
        table.append_column('new column', [u'Álvaro'.encode('iso-8859-1'),
                                           u'Píton'.encode('iso-8859-1')])
        self.assertEquals(table.headers, ['python', 'rules', 'new column'])
        self.assertEquals(table[:], [[1, 2, u'Álvaro'], [3, 4, u'Píton']])

    def test_append_column_should_be_inserted_in_any_position(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4]])
        table.append_column('new column', [3, 5], position=0)
        self.assertEquals(table.headers, ['new column', 'python', 'rules'])
        self.assertEquals(table[:], [[3, 1, 2], [5, 3, 4]])

    def test_append_column_should_accept_a_function_to_create_new_column(self):
        table = Table(headers=['python', 'rules'])
        table.extend([[1, 2], [3, 4]])
        table.append_column('new column', lambda row: row[0] + row[1])
        self.assertEquals(table.headers, ['python', 'rules', 'new column'])
        self.assertEquals(table[:], [[1, 2, 3], [3, 4, 7]])
        del table['new column']

        table.append_column('other column', lambda row: row[0] + row[1],
                            position=0)
        self.assertEquals(table.headers, ['other column', 'python', 'rules'])
        self.assertEquals(table[:], [[3, 1, 2], [7, 3, 4]])
        del table['other column']

        table.append_column('third column', lambda r: r['python'] * r['rules'],
                            row_as_dict=True)
        self.assertEquals(table.headers, ['python', 'rules', 'third column'])
        self.assertEquals(table[:], [[1, 2, 2], [3, 4, 12]])

    #TODO:
    # - Plugins: before call `write`, verify if `table.headers` exists
