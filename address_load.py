#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: address_load.py                                                         *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                                     *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 4/15/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
from functions import create_connection
from datetime import datetime
import json
from psycopg2 import errors

def main(key, address):

    with open('info.json', 'r') as f:
        info = json.load(f)

    db_name = info['psql']['db_name']
    db_user = info['psql']['db_user']
    db_password = info['psql']['db_password']
    db_host = info['psql']['db_host']
    db_port = info['psql']['db_port']

    connection = create_connection(db_name, db_user, db_password, db_host, db_port)
    cursor = connection.cursor()

    comment = ''
    created_time = datetime.now()
    updated_time = created_time

    query = """
    INSERT INTO address (address_type, addresses, comment, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)
    RETURNING address_id;
    
    """



    values = (key, address, comment, created_time, updated_time)
    try:
        cursor.execute(query, values)
        address_id = cursor.fetchone()[0]

    except errors.UniqueViolation as e:
        connection.rollback()
        search_query = f"SELECT address_id FROM address WHERE addresses = '{address}'"
        cursor.execute(search_query)
        address_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()
    return address_id

if __name__ == '__main__':
    main(key, address)
