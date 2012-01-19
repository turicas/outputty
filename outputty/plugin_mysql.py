#!/usr/bin/env python
# coding: utf-8

import datetime
import MySQLdb


MYSQL_TYPE = {str: 'TEXT', int: 'INT', float: 'FLOAT', datetime.date: 'DATE',
              datetime.datetime: 'DATETIME'}
MYSQLDB_TYPE = {getattr(MySQLdb.FIELD_TYPE, x): x \
                for x in dir(MySQLdb.FIELD_TYPE) if not x.startswith('_')}
MYSQLDB_TO_PYTHON = {'ENUM': str,
                     'STRING': str,
                     'VAR_STRING': str,
                     'BLOB': bytes,
                     'LONG_BLOB': bytes,
                     'MEDIUM_BLOB': bytes,
                     'TINY_BLOB': bytes,
                     'DECIMAL': float,
                     'DOUBLE': float,
                     'FLOAT': float,
                     'INT24': int,
                     'LONG': int,
                     'LONGLONG': int,
                     'TINY': int,
                     'YEAR': int,
                     'DATE': datetime.date,
                     'NEWDATE': datetime.date,
                     'TIME': int,
                     'TIMESTAMP': int,
                     'DATETIME': datetime.datetime}

def _get_mysql_config(connection_str):
    colon_index = connection_str.index(':')
    at_index = connection_str.index('@')
    slash_index = connection_str.index('/')
    config = {}
    config['user'] = connection_str[:colon_index]
    config['passwd'] = connection_str[colon_index + 1:at_index]
    config['host'] = connection_str[at_index + 1:slash_index]
    config['port'] = 3306
    if ':' in config['host']:
        data = config['host'].split(':')
        config['host'] = data[0]
        config['port'] = int(data[1])
    if connection_str.count('/') == 1:
        table_name = None
        config['db'] = connection_str[slash_index + 1:]
    else:
        second_slash_index = connection_str.index('/', slash_index + 1)
        config['db'] = connection_str[slash_index + 1:second_slash_index]
        table_name = connection_str[second_slash_index + 1:]
    return config, table_name

def _connect_to_mysql(config):
    return MySQLdb.connect(**config)

def read(table, connection_string, limit=None, order_by=None, query=''):
    config, table_name = _get_mysql_config(connection_string)
    connection = _connect_to_mysql(config)
    cursor = connection.cursor()
    if query:
        sql = query
    else:
        sql = 'SELECT * FROM ' + table_name
        if limit is not None:
            sql += ' LIMIT {0[0]}, {0[1]}'.format(limit)
        if order_by is not None:
            sql += ' ORDER BY ' + order_by
    cursor.execute(sql)
    column_info = [(x[0], x[1]) for x in cursor.description]
    table.headers = [x[0] for x in cursor.description]
    table.types = {name: MYSQLDB_TO_PYTHON[MYSQLDB_TYPE[type_]] \
                   for name, type_ in column_info}
    table._rows = [list(row) for row in cursor.fetchall()]
    cursor.close()
    connection.close()

def write(table, connection_string):
    config, table_name = _get_mysql_config(connection_string)
    connection = _connect_to_mysql(config)
    db_encoding = connection.character_set_name()
    escape_string = connection.escape_string
    table._identify_type_of_data()
    columns_and_types = []
    for header in table.headers:
        mysql_type = MYSQL_TYPE[table.types[header]]
        columns_and_types.append(header + ' ' + mysql_type)
    table_cols = ', '.join(columns_and_types)
    sql = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(table_name, table_cols)
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
