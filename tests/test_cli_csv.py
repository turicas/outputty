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
from textwrap import dedent
from utils import execute
from base_cli_writer import OutputtyCliWriter


class TestOutputtyCliCsvWriter(OutputtyCliWriter, unittest.TestCase):
    plugin_name = 'csv'


class TestOutputtyCliCsvReader(unittest.TestCase):
    def test_outputty_with_table_should_receive_data_from_stdin(self):
        out, err, code = execute('--read-csv', 'a\n')
        self.assertEquals(out, dedent('''
        +---+
        | a |
        +---+
        ''').strip() + '\n')

    def test_read_csv_without_filename_should_ignore_this_option(self):
        out, err, code = execute('--read-csv', 'a,b\n1,2\n')
        self.assertEquals(out, dedent('''
        +---+---+
        | a | b |
        +---+---+
        | 1 | 2 |
        +---+---+
        ''').strip() + '\n')

    def test_read_csv_with_filename_should_print_correctly_data(self):
        temp_fp = tempfile.NamedTemporaryFile()
        temp_fp.write("spam,eggs\nham,spam\neggs,ham")
        temp_fp.seek(0)
        out, err, code = execute('--read-csv ' + temp_fp.name)
        temp_fp.close()
        self.assertEquals(out, dedent('''
        +------+------+
        | spam | eggs |
        +------+------+
        |  ham | spam |
        | eggs |  ham |
        +------+------+
        ''').strip() + '\n')

    def test_read_csv_with_wrong_filename_returns_1_and_stderr_not_empty(self):
        out, err, code = execute('--read-csv doesnt-exist')
        expected_error = "[Errno 2] No such file or directory: 'doesnt-exist'\n"
        self.assertEquals(code, 1)
        self.assertEquals(err, expected_error)

    def test_read_csv_without_permissions_returns_1_and_stderr_not_empty(self):
        out, err, code = execute('--read-csv /root/test', 'a,b\n1,2')
        expected_error = "[Errno 13] Permission denied: '/root/test'\n"
        self.assertEquals(code, 1)
        self.assertEquals(err, expected_error)

    def test_read_stdin_with_input_encoding(self):
        input_string = u'álvaro\ntesting'.encode('utf16')
        out, err, code = execute('--read-csv --input-encoding utf16',
                                 input_string)
        self.assertEquals(out, dedent('''
        +---------+
        |  álvaro |
        +---------+
        | testing |
        +---------+
        ''').strip() + '\n')
