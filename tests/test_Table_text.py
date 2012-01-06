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
import tempfile
import os
from outputty import Table


class TestTableTxt(unittest.TestCase):
    def test_should_save_data_into_text_file(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.close()

        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.append({'ham': '', 'spam': '', 'eggs': ''})
        my_table.append({'ham': 1, 'spam': 2, 'eggs': 3})
        my_table.append({'ham': 11, 'spam': 22, 'eggs': 33})

        my_table.write('text', temp_fp.name)
        output = my_table.write('text')
        fp = open(temp_fp.name, 'r')
        contents = fp.read()
        fp.close()
        os.remove(temp_fp.name)
        self.assertEqual(contents, dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        |     |      |      |
        |   1 |    2 |    3 |
        |  11 |   22 |   33 |
        +-----+------+------+
        ''').strip())
        self.assertEquals(contents, output)

    def test_input_and_output_character_encoding_in_method_to_text_file(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.close()
        my_table = Table(headers=['Álvaro'.decode('utf8').encode('utf16')],
                         input_encoding='utf16', output_encoding='iso-8859-1')
        my_table.append(['Píton'.decode('utf8').encode('utf16')])
        my_table.write('text', temp_fp.name)

        fp = open(temp_fp.name)
        file_contents = fp.read()
        fp.close()
        os.remove(temp_fp.name)
        output = dedent('''
        +--------+
        | Álvaro |
        +--------+
        |  Píton |
        +--------+
        ''').strip().decode('utf8').encode('iso-8859-1')
        self.assertEqual(file_contents, output)

        #TODO: test input and output encoding
