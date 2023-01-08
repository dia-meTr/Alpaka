import os


type_groups = {
    'CHAR': 'string',
    'VARCHAR': 'string',
    'ENUM': 'string',
    'VAR_STRING': 'string',
    'STRING': 'string',
    'MEDIUMBLOB': 'string',
    'LONGBLOB': 'string',
    'TINYTEXT': 'string',
    'TEXT': 'string',
    'MEDIUMTEXT': 'string',
    'LONGTEXT': 'string',
    'SET': 'string',

    'TINY_BLOB': 'binary',
    'MEDIUM_BLOB': 'binary',
    'LONG_BLOB': 'binary',
    'BLOB': 'binary',
    'BINARY': 'binary',
    'VARBINARY': 'binary',
    'TINYBLOB': 'binary',

    'TINYINT': 'number',
    'SMALLINT': 'number',
    'MEDIUMINT': 'number',
    'INT': 'number',
    'BIGINT': 'number',
    'DECIMAL': 'number',
    'NEWDECIMAL': 'number',
    'TINY': 'number',
    'SHORT': 'number',
    'LONG': 'number',
    'LONGLONG': 'number',
    'INT24': 'number',
    'BIT': 'number',
    'YEAR': 'number',

    'REAL': 'float',
    'FLOAT': 'float',
    'DOUBLE': 'float',

    'DATE': 'datetime',
    'TIME': 'datetime',
    'DATETIME': 'datetime',
    'TIMESTAMP': 'datetime',
}

script_dir = os.path.dirname(__file__)

api_link = "http://127.0.0.1:5000/api/v1/"
