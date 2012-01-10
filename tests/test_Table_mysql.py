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
import tempfile
import os
from outputty import Table
import MySQLdb
import sqlite3


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
        plugin_mysql = table._load_plugin('mysql')
        plugin_mysql._get_mysql_config(table, 'u:p@h/d/t')
        self.assertEquals(table.mysql_username, 'u')
        self.assertEquals(table.mysql_password, 'p')
        self.assertEquals(table.mysql_hostname, 'h')
        self.assertEquals(table.mysql_port, 3306)
        self.assertEquals(table.mysql_database, 'd')
        self.assertEquals(table.mysql_table, 't')

    def test_connection_parameters_with_changed_port(self):
        table = Table()
        plugin_mysql = table._load_plugin('mysql')
        plugin_mysql._get_mysql_config(table, 'u:p@h:0/d/t')
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
        table = Table()
        table.read('mysql', self.connection_string)
        self.assertEquals(str(table), dedent('''
        +--------+--------+
        | field1 | field2 |
        +--------+--------+
        |    123 |      a |
        |    456 |      b |
        |    789 |      c |
        +--------+--------+
        ''').strip())

    def test_from_mysql_should_get_data_with_correct_types(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.query('CREATE TABLE %s (a INT(11), b FLOAT, c DATE, \
                               d DATETIME, e TEXT)' % self.table)
        self.connection.query('INSERT INTO %s VALUES (1, 3.14, "2011-11-11", \
                               "2011-11-11 11:11:11", "Python")' % self.table)
        table = Table()
        table.read('mysql', self.connection_string)
        int_value = table[0][0]
        float_value = table[0][1]
        date_value = table[0][2]
        datetime_value = table[0][3]
        text_value = table[0][4]
        self.assertIn(type(int_value), (type(1), type(1L)))
        self.assertEquals(type(float_value), type(1.0))
        self.assertEquals(type(date_value), type(datetime.date(2011, 11, 11)))
        self.assertEquals(type(datetime_value),
                          type(datetime.datetime(2011, 11, 11, 11, 11, 11)))
        self.assertEquals(type(text_value), type(''))

    def test_to_mysql_should_create_table_even_if_only_headers_present(self):
        self.connection.query('DROP TABLE ' + self.table)
        table = Table(headers=['spam', 'eggs'])
        table.write('mysql', self.connection_string)
        self.cursor.execute('SELECT * FROM ' + self.table)
        cols = [x[0] for x in self.cursor.description]
        self.assertEquals(set(cols), set(['spam', 'eggs']))

    def test_to_mysql_should_not_create_table_if_it_exists(self):
        table = Table()
        table.write('mysql', self.connection_string)
        self.cursor.execute('SELECT * FROM ' + self.table)
        cols = [x[0] for x in self.cursor.description]
        self.assertEquals(set(cols), set(['field1', 'field2']))

    def test_to_mysql_should_add_rows_correctly(self):
        self.connection.query('DROP TABLE ' + self.table)
        table = Table(headers=['spam', 'eggs'])
        table.append(['python', 'rules'])
        table.append(['free software', 'ownz'])
        table.write('mysql', self.connection_string)
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
        table.append(['spam eggs', 1])
        table.append(['spam spam', 3.14])
        table.append(['eggs spam', 'testing'])
        table.append(['spam spam', '2011-11-23'])
        table.append(['spam  ham', '2011-11-23 02:00:17'])
        table._identify_type_of_data()
        self.assertEqual(table.types['eggs'], str)
        self.assertEqual(table.types['ham'], str)

    def test_should_indentify_type_int_correctly(self):
        table = Table(headers=['spam'])
        table.append([1])
        table.append([2])
        table._identify_type_of_data()
        self.assertEqual(table.types['spam'], int)

    def test_should_not_indentify_non_fractional_floats_as_int(self):
        table = Table(headers=['ham'])
        table.append([1.0])
        table.append([2.0])
        table.append([3.0])
        table._identify_type_of_data()
        self.assertEqual(table.types['ham'], float)

    def test_should_indentify_type_float_correctly(self):
        table = Table(headers=['ham'])
        table.append([1.0])
        table.append([3.14])
        table._identify_type_of_data()
        self.assertEqual(table.types['ham'], float)

    def test_should_indentify_type_date_correctly(self):
        table = Table(headers=['Python'])
        table.append(['2010-11-15'])
        table.append(['2011-11-20'])
        table._identify_type_of_data()
        self.assertEqual(table.types['Python'], datetime.date)

    def test_should_indentify_type_datetime_correctly(self):
        table = Table(headers=['Monty'])
        table.append(['2010-11-15 02:42:01'])
        table.append(['2011-11-20 21:05:59'])
        table._identify_type_of_data()
        self.assertEqual(table.types['Monty'], datetime.datetime)

    def test_None_should_not_affect_data_type(self):
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python'])
        table.append([1, 2.71, '2011-01-01', '2011-01-01 00:00:00', 'asd'])
        table.append([None, None, None, None, None])
        table._identify_type_of_data()
        self.assertEquals(table.types['spam'], int)
        self.assertEquals(table.types['eggs'], float)
        self.assertEquals(table.types['ham'], datetime.date)
        self.assertEquals(table.types['Monty'], datetime.datetime)
        self.assertEquals(table.types['Python'], str)

    def test_to_mysql_should_create_the_table_with_correct_data_types(self):
        self.connection.query('DROP TABLE ' + self.table)
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python'])
        table.append([1, 2.71, '2011-01-01', '2011-01-01 00:00:00', 'asd'])
        table.append([2, 3.14, '2011-01-02', '2011-01-01 00:00:01', 'fgh'])
        table.append([3, 1.23, '2011-01-03', '2011-01-01 00:00:02', 'jkl'])
        table.append([4, 4.56, '2011-01-04', '2011-01-01 00:00:03', 'qwe'])
        table.append([5, 7.89, '2011-01-05', '2011-01-01 00:00:04', 'rty'])
        table.write('mysql', self.connection_string)
        self.cursor.execute('DESCRIBE ' + self.table)
        data_types = dict([[x[0], x[1]] for x in self.cursor.fetchall()])
        self.assertTrue(data_types['spam'].startswith('int'))
        self.assertEquals(data_types['eggs'], 'float')
        self.assertEquals(data_types['ham'], 'date')
        self.assertEquals(data_types['Monty'], 'datetime')
        self.assertEquals(data_types['Python'], 'text')

    def test_None_should_be_saved_as_NULL_and_returned_as_None(self):
        self.connection.query('DROP TABLE ' + self.table)
        table = Table(headers=['spam', 'eggs', 'ham', 'Monty', 'Python'])
        table.append([1, 2.71, '2011-01-01', '2011-01-01 00:00:00', 'asd'])
        table.append([None, None, None, None, None])
        table.write('mysql', self.connection_string)
        self.cursor.execute('SELECT * FROM ' + self.table)
        rows = self.cursor.fetchall()
        for i in range(5):
            self.assertIs(rows[-1][i], None)

    def test_should_deal_correctly_with_quotes(self):
        self.connection.query('DROP TABLE ' + self.table)
        table = Table(headers=['eggs'])
        table.append(['spam"ham'])
        table.write('mysql', self.connection_string)
        table_2 = Table()
        table_2.read('mysql', self.connection_string)
        self.assertEquals(table_2[0][0], 'spam"ham')

    @unittest.skip('Not implemented')
    def test_should_import_from_any_python_db_api_compatible(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.close()
        filename = temp_fp.name
        sqlite_connection = sqlite3.connect(filename)
        sqlite_cursor = sqlite_connection.cursor()
        sqlite_cursor.execute('CREATE TABLE testing (spam INT, eggs TEXT)')
        sqlite_cursor.execute('INSERT INTO testing VALUES (42, "python")')
        sqlite_cursor.execute('INSERT INTO testing VALUES (43, "rules")')
        sqlite_connection.commit()
        sqlite_cursor.close()
        sqlite_connection.close()
        table = Table(from_database={'backend': 'sqlite', 'config': filename,
                                     'table': 'testing'})
        os.remove(filename)
        self.assertEquals(table[0][0], 42)
        self.assertEquals(table[0][1], 'python')
        self.assertEquals(table[1][0], 43)
        self.assertEquals(table[1][1], 'rules')

    @unittest.skip('not implemented')
    def test_should_deal_correctly_with_database_encoding(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.query('CREATE TABLE %s (spam TEXT, eggs TEXT)' % \
                              self.table)
        table = Table(headers=['spam', 'eggs'], input_encoding='utf16')
        table.rows.append([u'Álvaro'.encode('utf16'),
                           u'álvaro'.encode('utf16')])
        table.to_mysql(self.connection_string)
        self.cursor.execute('SELECT * FROM ' + self.table)
        rows = [x for x in self.cursor.fetchall()]
        db_encoding = self.connection.character_set_name()
        self.assertEquals(len(rows), 1)
        self.assertEquals(rows[0][0].decode(db_encoding), u'Álvaro')
        self.assertEquals(rows[0][1].decode(db_encoding), u'álvaro')

    #TODO:
    #deal with encodings
    #from/to_mysql with exception (cannot connect, wrong user/pass etc.)
    #to_mysql overrides data from from_mysql. what to do?
    #what if incompatible data types (self.rows vs table structure)?
    #what if MySQLdb is not installed?
    #should be lazy (don't put things in memory until needed)
