#!/usr/bin/env python
# coding: utf-8

import datetime
import MySQLdb


MYSQL_TYPE = {str: 'TEXT', int: 'INT', float: 'FLOAT', datetime.date: 'DATE',
              datetime.datetime: 'DATETIME'}


def _get_mysql_config(table, connection_str):
    colon_index = connection_str.index(':')
    at_index = connection_str.index('@')
    slash_index = connection_str.index('/')
    second_slash_index = connection_str.index('/', slash_index + 1)
    table.mysql_username = connection_str[:colon_index]
    table.mysql_password = connection_str[colon_index + 1:at_index]
    table.mysql_hostname = connection_str[at_index + 1:slash_index]
    table.mysql_port = 3306
    if ':' in table.mysql_hostname:
        data = table.mysql_hostname.split(':')
        table.mysql_hostname = data[0]
        table.mysql_port = int(data[1])
    table.mysql_database = connection_str[slash_index + 1:second_slash_index]
    table.mysql_table = connection_str[second_slash_index + 1:]

def _connect_to_mysql(table):
    table.mysql_connection = MySQLdb.connect(user=table.mysql_username,
            passwd=table.mysql_password, host=table.mysql_hostname,
            port=table.mysql_port, db=table.mysql_database)
    table.cursor = table.mysql_connection.cursor()

def read(table, connection_string):
    _get_mysql_config(table, connection_string)
    _connect_to_mysql(table)
    table.cursor.execute('SELECT * FROM ' + table.mysql_table)
    table.headers = [x[0] for x in table.cursor.description]
    table._rows = [row for row in table.cursor.fetchall()]
    table.mysql_connection.close()

def write(table, connection_string):
    _get_mysql_config(table, connection_string)
    table._identify_type_of_data()
    _connect_to_mysql(table)
    if table.headers:
        columns_and_types = ['%s %s' % (k, MYSQL_TYPE[v]) \
                             for k, v in table.types.iteritems()]
        sql = 'CREATE TABLE IF NOT EXISTS %s (%s)' % \
              (table.mysql_table, ', '.join(columns_and_types))
        table.mysql_connection.query(sql)
    for row in table:
        values = []
        for value in row:
            if value is None:
                value = 'NULL'
            else:
                value = '"%s"' % \
                        table.mysql_connection.escape_string(str(value))
            values.append(value)
        values_with_quotes = ', '.join(values)
        sql = 'INSERT INTO %s VALUES (%s)' % (table.mysql_table,
                                              values_with_quotes)
        table.mysql_connection.query(sql)
    table.mysql_connection.close()
