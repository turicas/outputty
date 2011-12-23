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
from utils import execute


class TestOutputtyCliBase(unittest.TestCase):
    def test_outputty_without_parameters_should_show_help(self):
        out, err, code = execute('')
        self.assertIn('import, filter and export data easily', out)
        self.assertIn('usage', out)
        self.assertIn('optional arguments', out)
        self.assertEqual(code, 0)

    def test_outputty_with_dash_h_or_doubledash_help_should_return_help(self):
        out, err, code = execute('-h')
        out_2, err_2, code_2 = execute('--help')
        self.assertIn('import, filter and export data easily', out)
        self.assertIn('import, filter and export data easily', out_2)
        self.assertIn('usage', out)
        self.assertIn('usage', out_2)
        self.assertIn('optional arguments', out)
        self.assertIn('optional arguments', out_2)
        self.assertEqual(code, 0)
        self.assertEqual(code_2, 0)
