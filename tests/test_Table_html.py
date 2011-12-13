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
from textwrap import dedent
from outputty import Table


class TestTableHtml(unittest.TestCase):
    def test_to_html_should_without_parameters_should_return_string(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        self.assertTrue(isinstance(my_table.to_html(), str))

    def test_to_html_with_only_headers(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        output = my_table.to_html(css_classes=False)
        expected = dedent('''
        <table>
          <tr>
            <th>ham</th>
            <th>spam</th>
            <th>eggs</th>
          </tr>
        </table>
        ''').strip()
        self.assertEquals(output, expected)

    def test_to_html_with_headers_and_some_rows(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append(['python', 'rules', '!'])
        my_table.rows.append({'ham': 'spam', 'spam': 'eggs', 'eggs': 'ham'})
        output = my_table.to_html(css_classes=False)
        expected = dedent('''
        <table>
          <tr>
            <th>ham</th>
            <th>spam</th>
            <th>eggs</th>
          </tr>
          <tr>
            <td>python</td>
            <td>rules</td>
            <td>!</td>
          </tr>
          <tr>
            <td>spam</td>
            <td>eggs</td>
            <td>ham</td>
          </tr>
        </table>
        ''').strip()
        self.assertEquals(output, expected)

    def test_to_html_with_headers_and_rows_with_some_columns_empty(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': 'spam'})
        my_table.rows.append({'spam': 'eggs'})
        my_table.rows.append({'eggs': 'ham'})
        output = my_table.to_html(css_classes=False)
        expected = dedent('''
        <table>
          <tr>
            <th>ham</th>
            <th>spam</th>
            <th>eggs</th>
          </tr>
          <tr>
            <td>spam</td>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td></td>
            <td>eggs</td>
            <td></td>
          </tr>
          <tr>
            <td></td>
            <td></td>
            <td>ham</td>
          </tr>
        </table>
        ''').strip()
        self.assertEquals(output, expected)

    def test_to_html_with_a_parameter_should_save_a_file(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.close()
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append(['python', 'rules', '!'])
        my_table.rows.append({'ham': 'spam', 'spam': 'eggs', 'eggs': 'ham'})
        my_table.to_html(temp_fp.name, css_classes=False)
        temp_fp = open(temp_fp.name)
        output = temp_fp.read()
        temp_fp.close()
        os.remove(temp_fp.name)
        expected = dedent('''
        <table>
          <tr>
            <th>ham</th>
            <th>spam</th>
            <th>eggs</th>
          </tr>
          <tr>
            <td>python</td>
            <td>rules</td>
            <td>!</td>
          </tr>
          <tr>
            <td>spam</td>
            <td>eggs</td>
            <td>ham</td>
          </tr>
        </table>
        ''').strip()
        self.assertEquals(output, expected)

    def test_to_html_should_create_CSS_classes_for_odd_and_even_rows(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append(['python', 'rules', '!'])
        my_table.rows.append({'ham': 'spam', 'spam': 'eggs', 'eggs': 'ham'})
        my_table.rows.append(['python', 'rules', '!'])
        my_table.rows.append({'ham': 'spam', 'spam': 'eggs', 'eggs': 'ham'})
        output = my_table.to_html(css_classes=True)
        expected = dedent('''
        <table>
          <tr class="header">
            <th>ham</th>
            <th>spam</th>
            <th>eggs</th>
          </tr>
          <tr class="odd">
            <td>python</td>
            <td>rules</td>
            <td>!</td>
          </tr>
          <tr class="even">
            <td>spam</td>
            <td>eggs</td>
            <td>ham</td>
          </tr>
          <tr class="odd">
            <td>python</td>
            <td>rules</td>
            <td>!</td>
          </tr>
          <tr class="even">
            <td>spam</td>
            <td>eggs</td>
            <td>ham</td>
          </tr>
        </table>
        ''').strip()
        self.assertEquals(output, expected)
