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
from utils import execute
from outputty import Table


class OutputtyCliWriter(object):
    def setUp(self):
        self.table = Table()
        self.data = 'álvaro,testing\n123,456\n'
        self.fp = tempfile.NamedTemporaryFile()
        self.fp.write(self.data)
        self.fp.seek(0)
        self.table.read('csv', self.fp)
        self.plugin = self.table._load_plugin(self.plugin_name)
        self.expected = self.plugin.write(self.table)
        self.clean_fp = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.fp.close()
        self.clean_fp.close()

    def test_should_read_csv_data_from_stdin_and_write_to_stdout(self):
        out, err, code = execute('--read-csv --write-' + self.plugin_name,
                                 self.data)
        self.assertEquals(out, self.expected)

    def test_should_read_csv_data_from_stdin_and_write_to_file(self):
        out, err, code = execute('--read-csv --write-%s %s' % \
                                 (self.plugin_name, self.clean_fp.name),
                                 self.data)
        self.clean_fp.seek(0)
        self.assertEquals(self.clean_fp.read(), self.expected)

    def test_write_with_wrong_filename_returns_2_and_stderr_not_empty(self):
        out, err, code = execute('--read-csv --write-%s /a/b/c' % \
                                 self.plugin_name, self.data)
        expected_error = "[Errno 2] No such file or directory: '/a/b/c'\n"
        self.assertEquals(code, 2)
        self.assertEquals(err, expected_error)

    def test_write_without_permissions_returns_2_and_stderr_not_empty(self):
        out, err, code = execute('--read-csv --write-%s /root/test' % \
                                 self.plugin_name, self.data)
        expected_error = "[Errno 13] Permission denied: '/root/test'\n"
        self.assertEquals(code, 2)
        self.assertEquals(err, expected_error)

    def test_output_encoding_should_work_both_in_stdout_and_file(self):
        out, err, code = execute('--read-csv --write-%s --output-encoding '
                                 'iso-8859-1' % self.plugin_name, self.data)
        out_2, err_2, code_2 = execute('--read-csv --write-%s %s '
                                       '--output-encoding iso-8859-1' % \
                                       (self.plugin_name, self.clean_fp.name),
                                       self.data)
        self.clean_fp.seek(0)
        expected = self.expected.decode('utf8').encode('iso-8859-1')
        self.assertEquals(out, expected)
        self.assertEquals(self.clean_fp.read(), expected)
