import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_to_db(filename) -> sqlite3.dbapi2.Connection:
    connection = sqlite3.connect(filename)
    connection.row_factory = dict_factory
    return connection