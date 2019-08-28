import mysql.connector
from utils import privatekeys, ddmdata
from mysql.connector import Error
from datetime import datetime


def connect():
    try:
        conn = mysql.connector.connect(host='homolog-distrito.cpwrmibgkvby.sa-east-1.rds.amazonaws.com',
                                       database='distrito_test',
                                       user=privatekeys.sqlUser,
                                       password=privatekeys.sqlPass,
                                       charset = 'utf8')
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
 
    except Error as e:
        print(repr(e))


def fo_query(query):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query)
 
        row = cursor.fetchone()
 
        while row is not None:
            print(row)
            row = cursor.fetchone()
 
    except Error as e:
        print(e)
 
    finally:
        cursor.close()
        conn.close()


def insert_csv(csvpath, tablename):
    entries = ddmdata.readcsv(csvpath)
    conn = connect()
    try:
        cursor = conn.cursor()
        for entry in entries:
            keysQuery = ''
            valuesQuery = ''
            items = entry.items()
            for item in items:
                key = item[0]
                value = item[1]
                try:
                    int(value)
                except:
                    if isinstance(value, str) and value.lower() != 'null':
                        value = '"{}"'.format(value)
                keysQuery += key + ', '
                valuesQuery += value + ', '
            cursor.execute('INSERT INTO {} ({}date_created)'.format(tablename, keysQuery) \
                + ' VALUES ({}"{}")'.format(valuesQuery, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
    except Exception as e:
        print(repr(e))
        print(entry)
    finally:
        conn.close()


def insert_csv_dateless(csvpath, tablename):
    entries = ddmdata.readcsv(csvpath)
    conn = connect()
    try:
        cursor = conn.cursor()
        for entry in entries:
            keysQuery = ''
            valuesQuery = ''
            items = entry.items()
            for i, item in enumerate(items):
                key = item[0]
                value = item[1]
                if isinstance(value, str) and value.lower() != 'null':
                    value = '"{}"'.format(value)
                if i == len(items) - 1:
                    keysQuery += key
                    valuesQuery += value
                else:
                    keysQuery += key + ', '
                    valuesQuery += value + ', '
            cursor.execute('INSERT INTO {} ({})'.format(tablename, keysQuery) \
                + ' VALUES ({})'.format(valuesQuery))
            conn.commit()
    except Exception as e:
        print(repr(e))
    finally:
        conn.close()

