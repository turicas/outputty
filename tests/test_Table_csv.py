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
import tempfile
import os
from cStringIO import StringIO
from textwrap import dedent
import types
import datetime
from outputty import Table


class TestTableCsv(unittest.TestCase):
    def test_write_csv_should_create_the_file_correctly_with_headers(self):
        temp_fp = tempfile.NamedTemporaryFile()
        temp_fp.close()

        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': 'ham spam ham', 'spam': 'spam eggs spam',
                              'eggs': 'eggs ham eggs'})
        my_table.write('csv', temp_fp.name)

        fp = open(temp_fp.name)
        contents = fp.read()
        fp.close()
        os.remove(temp_fp.name)

        self.assertEquals(contents, dedent('''\
        "ham","spam","eggs"
        "ham spam ham","spam eggs spam","eggs ham eggs"
        '''))

    def test_Table_should_accept_file_object_in_read_csv(self):
        csv_fake = StringIO()
        csv_fake.write(dedent('''\
        "ham","spam","eggs"
        "ham spam ham","spam eggs spam","eggs ham eggs"
        "ham spam","eggs spam","eggs eggs"
        '''))
        csv_fake.seek(0)
        my_table = Table()
        my_table.read('csv', csv_fake)
        self.assertEquals(str(my_table), dedent('''
        +--------------+----------------+---------------+
        |     ham      |      spam      |      eggs     |
        +--------------+----------------+---------------+
        | ham spam ham | spam eggs spam | eggs ham eggs |
        |     ham spam |      eggs spam |     eggs eggs |
        +--------------+----------------+---------------+
        ''').strip())


    def test_should_import_data_from_csv(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.write(dedent('''\
        "ham","spam","eggs"
        "ham spam ham","spam eggs spam","eggs ham eggs"
        "ham spam","eggs spam","eggs eggs"
        '''))
        temp_fp.close()

        my_table = Table()
        my_table.read('csv', temp_fp.name)
        os.remove(temp_fp.name)
        self.assertEquals(str(my_table), dedent('''
        +--------------+----------------+---------------+
        |     ham      |      spam      |      eggs     |
        +--------------+----------------+---------------+
        | ham spam ham | spam eggs spam | eggs ham eggs |
        |     ham spam |      eggs spam |     eggs eggs |
        +--------------+----------------+---------------+
        ''').strip())

    def test_should_import_data_from_csv_with_only_one_line(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.write(dedent('''\
        "ham","spam","eggs"
        '''))
        temp_fp.close()

        my_table = Table()
        my_table.read('csv', temp_fp.name)
        os.remove(temp_fp.name)
        self.assertEquals(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        ''').strip())

    def test_should_import_nothing_from_empty_csv_without_exceptions(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.close()

        my_table = Table()
        my_table.read('csv', temp_fp.name)
        os.remove(temp_fp.name)
        self.assertEquals(str(my_table), '')

    def test_input_and_output_encoding_should_affect_method_write_csv(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.close()
        my_table = Table(headers=['Álvaro'.decode('utf8').encode('utf16')],
                         input_encoding='utf16', output_encoding='iso-8859-1')
        my_table.rows.append(['Píton'.decode('utf8').encode('utf16')])
        my_table.write('csv', temp_fp.name)

        fp = open(temp_fp.name)
        file_contents = fp.read()
        fp.close()
        os.remove(temp_fp.name)
        output = '"Álvaro"\n"Píton"\n'.decode('utf8').encode('iso-8859-1')
        self.assertEqual(file_contents, output)

    def test_input_and_output_encoding_should_affect_read_csv(self):
        data = '"Álvaro"\n"Píton"'
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.write(data.decode('utf8').encode('iso-8859-1'))
        temp_fp.close()
        my_table = Table(input_encoding='iso-8859-1', output_encoding='utf16')
        my_table.read('csv', temp_fp.name)
        os.remove(temp_fp.name)
        output = dedent('''
        +--------+
        | Álvaro |
        +--------+
        |  Píton |
        +--------+
        ''').strip().decode('utf8').encode('utf16')
        self.assertEqual(str(my_table), output)

    def test_read_csv_should_accept_filepointer(self):
        data = '"Álvaro"\n"Píton"'
        temp_fp = tempfile.NamedTemporaryFile()
        temp_fp.write(data)
        temp_fp.seek(0)
        my_table = Table()
        my_table.read('csv', temp_fp)
        output = dedent('''
        +--------+
        | Álvaro |
        +--------+
        |  Píton |
        +--------+
        ''').strip()
        table_output = str(my_table)
        temp_fp.close()
        self.assertEqual(table_output, output)

    def test_input_encoding_should_affect_read_csv_when_using_filepointer(self):
        data = '"Álvaro"\n"Píton"'
        temp_fp = tempfile.NamedTemporaryFile()
        temp_fp.write(data.decode('utf8').encode('utf16'))
        temp_fp.seek(0)
        my_table = Table(input_encoding='utf16', output_encoding='iso-8859-1')
        my_table.read('csv', temp_fp)
        output = dedent('''
        +--------+
        | Álvaro |
        +--------+
        |  Píton |
        +--------+
        ''').strip().decode('utf8').encode('iso-8859-1')
        table_output = str(my_table)
        temp_fp.close()
        self.assertEqual(table_output, output)

    def test_read_csv_should_automatically_convert_data_types(self):
        data = dedent('''
        "spam","eggs","ham"
        "42","3","2011-01-02"
        "","3.14","2012-01-11"
        "21","","2010-01-03"
        "2","2.71",""
        ''')
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.write(data)
        temp_fp.close()
        my_table = Table()
        my_table.read('csv', temp_fp.name)
        os.remove(temp_fp.name)
        self.assertEquals(type(my_table.rows[0][0]), types.IntType)
        self.assertEquals(type(my_table.rows[1][0]), types.NoneType)
        self.assertEquals(type(my_table.rows[2][0]), types.IntType)
        self.assertEquals(type(my_table.rows[3][0]), types.IntType)
        self.assertEquals(type(my_table.rows[0][1]), types.FloatType)
        self.assertEquals(type(my_table.rows[1][1]), types.FloatType)
        self.assertEquals(type(my_table.rows[2][1]), types.NoneType)
        self.assertEquals(type(my_table.rows[3][1]), types.FloatType)
        self.assertEquals(type(my_table.rows[0][2]), datetime.date)
        self.assertEquals(type(my_table.rows[1][2]), datetime.date)
        self.assertEquals(type(my_table.rows[2][2]), datetime.date)
        self.assertEquals(type(my_table.rows[3][2]), types.NoneType)

    def test_read_csv_shouldnt_convert_types_when_convert_types_is_False(self):
        data = dedent('''
        "spam","eggs","ham"
        "42","3","2011-01-02"
        "","3.14","2012-01-11"
        "21","","2010-01-03"
        "2","2.71",""
        ''')
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.write(data)
        temp_fp.close()
        my_table = Table()
        my_table.read('csv', temp_fp.name, convert_types=False)
        os.remove(temp_fp.name)
        for row in my_table.rows:
            for value in row:
                self.assertEquals(type(value), types.UnicodeType)
