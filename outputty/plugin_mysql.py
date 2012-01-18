#!/usr/bin/env python
# coding: utf-8

import datetime
import MySQLdb


MYSQL_TYPE = {str: 'TEXT', int: 'INT', float: 'FLOAT', datetime.date: 'DATE',
              datetime.datetime: 'DATETIME'}


def _get_mysql_config(connection_str):
    colon_index = connection_str.index(':')
    at_index = connection_str.index('@')
    slash_index = connection_str.index('/')
    second_slash_index = connection_str.index('/', slash_index + 1)
    config = {}
    config['user'] = connection_str[:colon_index]
    config['passwd'] = connection_str[colon_index + 1:at_index]
    config['host'] = connection_str[at_index + 1:slash_index]
    config['port'] = 3306
    if ':' in config['host']:
        data = config['host'].split(':')
        config['host'] = data[0]
        config['port'] = int(data[1])
    config['db'] = connection_str[slash_index + 1:second_slash_index]
    table_name = connection_str[second_slash_index + 1:]
    return config, table_name

def _connect_to_mysql(config):
    return MySQLdb.connect(**config)

def read(table, connection_string, limit=None, order_by=None):
    config, table_name = _get_mysql_config(connection_string)
    connection = _connect_to_mysql(config)
    cursor = connection.cursor()
    sql = 'SELECT * FROM ' + table_name
    if limit is not None:
        sql += ' LIMIT {0[0]}, {0[1]}'.format(limit)
    if order_by is not None:
        sql += ' ORDER BY ' + order_by
    cursor.execute(sql)
    table.headers = [x[0] for x in cursor.description]
    table._rows = [list(row) for row in cursor.fetchall()]
    cursor.close()
    connection.close()

def write(table, connection_string):
    config, table_name = _get_mysql_config(connection_string)
    connection = _connect_to_mysql(config)
    db_encoding = connection.character_set_name()
    escape_string = connection.escape_string
    table._identify_type_of_data()
    if table.headers:
        columns_and_types = ['{} {}'.format(header,
                                            MYSQL_TYPE[table.types[header]]) \
                             for header in table.headers]
        sql = 'CREATE TABLE IF NOT EXISTS %s (%s)' % \
              (table_name, ', '.join(columns_and_types))
        connection.query(sql)
    for row in table:
        values = []
        for value in row:
            if value is None:
                value = 'NULL'
            else:
                value = escape_string(unicode(value).encode(db_encoding))
                value = '"' + value + '"'
            values.append(value)
        values_with_quotes = ', '.join(values)
        sql = 'INSERT INTO %s VALUES (%s)' % (table_name,
                                              values_with_quotes)
        connection.query(sql)
    connection.close()
