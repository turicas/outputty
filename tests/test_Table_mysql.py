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
import tempfile
import sqlite3
import os
from textwrap import dedent
from cStringIO import StringIO
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
        self.connection.commit()
        self.connection.close()

    def test_should_identify_connection_parameters(self):
        table = Table()
        plugin_mysql = table._load_plugin('mysql')
        config, table_name = plugin_mysql._get_mysql_config('u:p@h/d/t')
        self.assertEquals(config['user'], 'u')
        self.assertEquals(config['passwd'], 'p')
        self.assertEquals(config['host'], 'h')
        self.assertEquals(config['port'], 3306)
        self.assertEquals(config['db'], 'd')
        self.assertEquals(table_name, 't')

    def test_should_identify_connection_parameters_with_custom_port(self):
        table = Table()
        plugin_mysql = table._load_plugin('mysql')
        config, table_name = plugin_mysql._get_mysql_config('u:p@h:0/d/t')
        self.assertEquals(config['user'], 'u')
        self.assertEquals(config['passwd'], 'p')
        self.assertEquals(config['host'], 'h')
        self.assertEquals(config['port'], 0)
        self.assertEquals(config['db'], 'd')
        self.assertEquals(table_name, 't')

    def test_read_should_retrieve_data_from_table(self):
        self.connection.query('INSERT INTO %s VALUES (123, "a")' % self.table)
        self.connection.query('INSERT INTO %s VALUES (456, "b")' % self.table)
        self.connection.query('INSERT INTO %s VALUES (789, "c")' % self.table)
        self.connection.commit()
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

    def test_read_should_get_data_with_correct_types(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.query('CREATE TABLE %s (a INT(11), b FLOAT, c DATE, \
                               d DATETIME, e TEXT)' % self.table)
        self.connection.query('INSERT INTO %s VALUES (1, 3.14, "2011-11-11", \
                               "2011-11-11 11:11:11", "Python")' % self.table)
        self.connection.commit()
        table = Table()
        table.read('mysql', self.connection_string)
        int_value = table[0][0]
        float_value = table[0][1]
        date_value = table[0][2]
        datetime_value = table[0][3]
        text_value = table[0][4]
        self.assertIn(type(int_value), (int, long))
        self.assertEquals(type(float_value), float)
        self.assertEquals(type(date_value), datetime.date)
        self.assertEquals(type(datetime_value),datetime.datetime)
        self.assertEquals(type(text_value), unicode)

    def test_write_should_create_table_even_if_only_headers_present(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.commit()
        table = Table(headers=['spam', 'eggs'])
        table.write('mysql', self.connection_string)
        self.cursor.execute('SELECT * FROM ' + self.table)
        cols = [x[0] for x in self.cursor.description]
        self.assertEquals(set(cols), set(['spam', 'eggs']))

    def test_write_should_not_create_table_if_it_exists(self):
        table = Table(headers=['monty', 'python'])
        table.write('mysql', self.connection_string)
        self.cursor.execute('SELECT * FROM ' + self.table)
        cols = [x[0] for x in self.cursor.description]
        self.assertEquals(set(cols), set(['field1', 'field2']))

    def test_write_should_add_rows_correctly(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.commit()
        table = Table(headers=['spam', 'eggs'])
        table.append(['python', 'rules'])
        table.append(['free software', 'ownz'])
        table.write('mysql', self.connection_string)
        self.cursor.execute('SELECT * FROM ' + self.table)
        rows = [row for row in self.cursor.fetchall()]
        self.assertEquals(rows, [('python', 'rules'),
                                 ('free software', 'ownz')])

    def test_write_should_create_the_table_with_correct_data_types(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.commit()
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
        self.connection.commit()
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
        self.connection.commit()
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

    def test_should_deal_correctly_with_database_encoding(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.query('CREATE TABLE %s (spam TEXT, eggs TEXT)' % \
                              self.table)
        self.connection.commit()
        table = Table(headers=[u'spam', u'eggs'], input_encoding='utf16')
        table.append([u'Álvaro'.encode('utf16'),
                      u'álvaro'.encode('utf16')])
        table.write('mysql', self.connection_string)
        self.cursor.execute('SELECT * FROM ' + self.table)
        rows = [x for x in self.cursor.fetchall()]
        db_encoding = self.connection.character_set_name()
        self.assertEquals(len(rows), 1)
        self.assertEquals(rows[0][0].decode(db_encoding), u'Álvaro')
        self.assertEquals(rows[0][1].decode(db_encoding), u'álvaro')
        self.assertEquals(table[0][0], u'Álvaro')
        self.assertEquals(table[0][1], u'álvaro')

    def test_should_insert_data_in_correct_order(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.commit()
        table = Table(headers=['name', 'age'])
        table.append(['Justen', 24])
        table.append(['Someone', 99])
        table.write('mysql', self.connection_string)
        self.cursor.execute('SELECT * FROM ' + self.table)
        rows = [x for x in self.cursor.fetchall()]
        self.assertEquals(len(rows), 2)
        self.assertEquals(rows[0][0], 'Justen')
        self.assertEquals(rows[0][1], 24)
        self.assertEquals(rows[1][0], 'Someone')
        self.assertEquals(rows[1][1], 99)

    def test_read_should_accept_limit(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.commit()
        table = Table(headers=['number'])
        numbers = range(1000)
        for i in numbers:
            table.append([i])
        table.write('mysql', self.connection_string)
        new_table = Table()
        new_table.read('mysql', self.connection_string, limit=(10, 100))
        self.assertEquals(new_table[:], [[x] for x in numbers[10:110]])

    def test_read_should_accept_order_by(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.commit()
        table = Table(headers=['number'])
        numbers = range(1000)
        for i in numbers:
            table.append([i])
        table.write('mysql', self.connection_string)
        new_table = Table()
        new_table.read('mysql', self.connection_string, order_by='number desc')
        self.assertEquals(new_table[:], [[x] for x in numbers[::-1]])

    def test_read_should_accept_a_SQL_instead_of_table_name(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.commit()
        table = Table(headers=['number'])
        numbers = range(1000)
        for i in numbers:
            table.append([i])
        table.write('mysql', self.connection_string)
        connection_string = '/'.join(self.connection_string.split('/')[:-1])
        new_table = Table()
        sql = ('SELECT * FROM {} WHERE number > 500 AND number < 510 ORDER BY '
               'number DESC LIMIT 2, 10')
        new_table.read('mysql', connection_string,
                       query=sql.format(self.table))
        self.assertEquals(new_table[:], [[x] for x in range(507, 500, -1)])

    def test_read_should_automatically_identify_data_types(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.commit()
        table = Table(headers=['spam', 'eggs', 'ham', 'monty', 'python'])
        numbers = range(1000)
        for i in numbers:
            table.append([i, i + 0.1, 'some string', '2012-01-01',
                          '2011-12-31 23:59:59'])
        table.write('mysql', self.connection_string)
        new_table = Table()
        new_table.read('mysql', self.connection_string)
        self.assertEquals(len(new_table), 1000)
        self.assertEquals(new_table.types['spam'], int)
        self.assertEquals(new_table.types['eggs'], float)
        self.assertEquals(new_table.types['ham'], str)
        self.assertEquals(new_table.types['monty'], datetime.date)
        self.assertEquals(new_table.types['python'], datetime.datetime)

        connection_string = '/'.join(self.connection_string.split('/')[:-1])
        other_table = Table()
        other_table.read('mysql', connection_string,
                         query='SELECT spam, ham, python FROM ' + self.table)
        self.assertEquals(len(other_table), 1000)
        self.assertEquals(len(other_table.types), 3)
        self.assertEquals(other_table.types['spam'], int)
        self.assertEquals(other_table.types['ham'], str)
        self.assertEquals(other_table.types['python'], datetime.datetime)

    def test_importing_from_csv_and_exporting_to_mysql_should_handle_types_correctly(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.commit()
        csv_fp = StringIO()
        csv_fp.write(dedent('''
        int_col,float_col,str_col,date_col,datetime_col
        1,1.2,abc,2012-04-01,2009-04-01 00:01:02
        2,2.3,cba,2011-03-02,2010-03-02 01:02:03
        3,3.4,bca,2010-02-03,2011-02-03 02:03:04
        4,4.5,cab,2009-01-04,2012-01-04 03:04:05
        '''))
        csv_fp.seek(0)
        table = Table()
        table.read('csv', csv_fp)
        table.write('mysql', self.connection_string)
        self.assertEquals(table.types['int_col'], int)
        self.assertEquals(table.types['float_col'], float)
        self.assertEquals(table.types['str_col'], str)
        self.assertEquals(table.types['date_col'], datetime.date)
        self.assertEquals(table.types['datetime_col'], datetime.datetime)

    def test_write_should_slugfy_column_names(self):
        self.connection.query('DROP TABLE ' + self.table)
        self.connection.commit()
        table = Table(headers=['col with  spaces', 'col-with-dashes'])
        table.append(['testing', 123])
        table.append(['testing again', 456])
        table.write('mysql', self.connection_string)

        other_table = Table()
        other_table.read('mysql', self.connection_string)
        self.assertEquals(other_table.headers, ['col_with_spaces',
                                                'col_with_dashes'])

    #TODO:
    # - write: use only one INSERT for all rows (before: check performance) -
    #   batch=True|False
    # - read: add 'ignore' parameter (to ignore some columns)
    # - write: Raise ValueError if table._rows is not compatible with table
    #   structure (already created)
    # - read/write: Raise exception when cannot connect, wrong user/pass etc.
    # - read/write: Option to do not close the connection so we can re-use it
