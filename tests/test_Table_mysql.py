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
    def setUp(self):
        self.username = 'root'
        self.password = 'r00t'
        self.hostname = 'localhost'
        self.database = 'outputty_test'
        self.table = 'temp_table'
        self.connection_string = '%s:%s@%s/%s/%s' % (self.username,
                self.password, self.hostname, self.database, self.table)

        self.connection = MySQLdb.connect(user=self.username,
                                         passwd=self.password,
                                         host=self.hostname)

        self.connection.query('DROP DATABASE IF EXISTS ' + self.database)
        self.connection.query('CREATE DATABASE ' + self.database)
        self.connection.select_db(self.database)
        self.cursor = self.connection.cursor()
        create_table = 'CREATE TABLE %s (field1 INT, field2 CHAR)' % self.table
        self.cursor.execute(create_table)

    def tearDown(self):
        self.connection.query('DROP DATABASE IF EXISTS ' + self.database)
        self.connection.close()

    def test_connection_parameters(self):
        table = Table()
        table._get_mysql_config('username:password@hostname/database/table')
        self.assertEquals(table.mysql_username, 'username')
        self.assertEquals(table.mysql_password, 'password')
        self.assertEquals(table.mysql_hostname, 'hostname')
        self.assertEquals(table.mysql_port, 3306)
        self.assertEquals(table.mysql_database, 'database')
        self.assertEquals(table.mysql_table, 'table')

    def test_from_mysql_should_retrieve_data_from_table(self):
        self.connection.query('INSERT INTO %s VALUES (123, "a")' % self.table)
        self.connection.query('INSERT INTO %s VALUES (456, "b")' % self.table)
        self.connection.query('INSERT INTO %s VALUES (789, "c")' % self.table)
        table = Table(from_mysql=self.connection_string)

        self.assertEquals(str(table), dedent('''
        +--------+--------+
        | field1 | field2 |
        +--------+--------+
        |    123 |      a |
        |    456 |      b |
        |    789 |      c |
        +--------+--------+
        ''').strip())

    #TODO:    
    #Change all values (including port) on connection string
    #from_mysql
    #to_mysql
    #from/to_mysql with exception (cannot connect, wrong user/pass etc.)
    #encodings
    #what if MySQLdb is not installed?
