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
import datetime
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

    def test_connection_parameters_with_changed_port(self):
        table = Table()
        table._get_mysql_config('u:p@h:0/d/t')
        self.assertEquals(table.mysql_username, 'u')
        self.assertEquals(table.mysql_password, 'p')
        self.assertEquals(table.mysql_hostname, 'h')
        self.assertEquals(table.mysql_port, 0)
        self.assertEquals(table.mysql_database, 'd')
        self.assertEquals(table.mysql_table, 't')

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

    def test_to_mysql_should_create_table_even_if_only_headers_present(self):
        self.connection.query('DROP TABLE ' + self.table)
        table = Table(headers=['spam', 'eggs'])
        table.to_mysql(self.connection_string)

        self.cursor.execute('SELECT * FROM ' + self.table)
        cols = [x[0] for x in self.cursor.description]
        self.assertEquals(set(cols), set(['spam', 'eggs']))

    def test_to_mysql_should_not_create_table_if_it_exists(self):
        table = Table()
        table.to_mysql(self.connection_string)

        self.cursor.execute('SELECT * FROM ' + self.table)
        cols = [x[0] for x in self.cursor.description]
        self.assertEquals(set(cols), set(['field1', 'field2']))

    def test_to_mysql_should_add_rows_correctly(self):
        self.connection.query('DROP TABLE ' + self.table)
        table = Table(headers=['spam', 'eggs'])
        table.rows.append(['python', 'rules'])
        table.rows.append(['free software', 'ownz'])
        table.to_mysql(self.connection_string)

        self.cursor.execute('SELECT * FROM ' + self.table)
        rows = [row for row in self.cursor.fetchall()]
        self.assertEquals(rows, [('python', 'rules'),
                                 ('free software', 'ownz')])

    def test_should_indentify_type_str_when_only_headers_present(self):
        table = Table(headers=['eggs', 'ham'])
        table._identify_type_of_data()
        self.assertEqual(table.types['eggs'], str)
        self.assertEqual(table.types['ham'], str)

    def test_should_indentify_type_str_correctly(self):
        table = Table(headers=['eggs', 'ham'])
        table.rows.append(['spam eggs', 1])
        table.rows.append(['spam spam', 3.14])
        table.rows.append(['eggs spam', 'testing'])
        table.rows.append(['spam spam', '2011-11-23'])
        table.rows.append(['spam  ham', '2011-11-23 02:00:17'])
        table._identify_type_of_data()
        self.assertEqual(table.types['eggs'], str)
        self.assertEqual(table.types['ham'], str)

    def test_should_indentify_type_int_correctly(self):
        table = Table(headers=['spam'])
        table.rows.append([1])
        table.rows.append([2])
        table._identify_type_of_data()
        self.assertEqual(table.types['spam'], int)

    def test_should_indentify_type_float_correctly(self):
        table = Table(headers=['ham'])
        table.rows.append([1.0])
        table.rows.append([3.14])
        table._identify_type_of_data()
        self.assertEqual(table.types['ham'], float)

    def test_should_indentify_type_date_correctly(self):
        table = Table(headers=['Python'])
        table.rows.append(['2010-11-15'])
        table.rows.append(['2011-11-20'])
        table._identify_type_of_data()
        self.assertEqual(table.types['Python'], datetime.date)

    def test_should_indentify_type_datetime_correctly(self):
        table = Table(headers=['Monty'])
        table.rows.append(['2010-11-15 02:42:01'])
        table.rows.append(['2011-11-20 21:05:59'])
        table._identify_type_of_data()
        self.assertEqual(table.types['Monty'], datetime.datetime)

    def test_to_mysql_should_create_the_table_with_correct_data_types(self):
        self.connection.query('DROP TABLE ' + self.table)
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python'])
        table.rows.append([1, 2.71, '2011-01-01', '2011-01-01 00:00:00', 'asd'])
        table.rows.append([2, 3.14, '2011-01-02', '2011-01-01 00:00:01', 'fgh'])
        table.rows.append([3, 1.23, '2011-01-03', '2011-01-01 00:00:02', 'jkl'])
        table.rows.append([4, 4.56, '2011-01-04', '2011-01-01 00:00:03', 'qwe'])
        table.rows.append([5, 7.89, '2011-01-05', '2011-01-01 00:00:04', 'rty'])
        table.to_mysql(self.connection_string)

        self.cursor.execute('DESCRIBE ' + self.table)
        data_types = dict([[x[0], x[1]] for x in self.cursor.fetchall()])
        self.assertTrue(data_types['spam'].startswith('int'))
        self.assertEquals(data_types['eggs'], 'float')
        self.assertEquals(data_types['ham'], 'date')
        self.assertEquals(data_types['Monty'], 'datetime')
        self.assertEquals(data_types['Python'], 'text')


    #TODO:
    #to_mysql overrides data from from_mysql. what to do?
    #what if data have quotes? use MySQLdb.escape_string
    #what if incompatible data types (self.rows vs table structure)?
    #from/to_mysql with exception (cannot connect, wrong user/pass etc.)
    #deal with encodings
    #what if MySQLdb is not installed?
