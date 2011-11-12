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

import subprocess
import shlex
import unittest
import os
import tempfile
from textwrap import dedent


TESTS_PATH = os.path.dirname(__file__)
OUTPUTTY_EXECUTABLE = os.path.join(TESTS_PATH, '../outputty')

def sh(command, finalize=True):
    process = subprocess.Popen(shlex.split(command), stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    if finalize:
        process.wait()
        process.out = process.stdout.read()
        process.err = process.stderr.read()
    return process

def execute(arguments='', stdin=''):
    process = sh(OUTPUTTY_EXECUTABLE + ' ' + arguments, finalize=False)
    process.stdin.write(stdin)
    process.stdin.close()
    process.wait()
    return process.stdout.read()

class TestOutputtyCli(unittest.TestCase):
    def test_outputty_command_should_run(self):
        process = sh(OUTPUTTY_EXECUTABLE)
        self.assertEquals(process.returncode, 0)
        self.assertEquals(process.err, '')

    def test_outputty_without_parameters_should_return_help(self):
        output = execute()
        help_string = 'Show data in terminal in a beautiful way, with Python'
        self.assertIn(help_string, output)
        self.assertIn('usage', output)
        self.assertIn('optional arguments', output)

    def test_outputty_with_table_should_receive_data_from_stdin(self):
        output = execute('--table', 'a\n')
        self.assertEquals(output, dedent('''
        +---+
        | a |
        +---+
        ''').strip() + '\n')

    def test_outputty_should_pretty_print_table_from_csv_data_in_stdin(self):
        output = execute('--table', 'a,b\n1,2\n')
        self.assertEquals(output, dedent('''
        +---+---+
        | a | b |
        +---+---+
        | 1 | 2 |
        +---+---+
        ''').strip() + '\n')

    def test_receive_csv_data_in_stdin_and_save_in_a_csv_file(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.close()
        output = execute('--table --to-csv ' + temp_fp.name, 'a,b\n1,2\n')
        temp_fp = open(temp_fp.name)
        csv_contents = temp_fp.read()
        os.remove(temp_fp.name)
        self.assertEquals(csv_contents, dedent('''
        "a","b"
        "1","2"
        ''').strip() + '\n')
