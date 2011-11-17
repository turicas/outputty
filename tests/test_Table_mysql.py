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
from textwrap import dedent
from outputty import Table
import MySQLdb


class TestTableMySQL(unittest.TestCase):
    def test_connection_parameters(self):
        table = Table(from_mysql='username:password@hostname/database/table')
        self.assertEquals(table.mysql_username, 'username')
        self.assertEquals(table.mysql_password, 'password')
        self.assertEquals(table.mysql_hostname, 'hostname')
        self.assertEquals(table.mysql_port, 3306)
        self.assertEquals(table.mysql_database, 'database')
        self.assertEquals(table.mysql_table, 'table')
