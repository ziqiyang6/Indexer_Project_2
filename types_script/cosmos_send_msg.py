# !/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_send_msg.py                                *
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
Version: 1.1                                                                        *
For 'cursor.execute' command, there is 'try' and 'except' to catch UniqueViolation  *
And if UniqueViolation happens, there will be search query to search needed value   *
New package: psycopg2 now applies on this script                                    *
New column 'comment' for transaction table has been added                           *                                                                                    *
                                                                                    *
                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
from functions import create_connection
import json
from psycopg2 import errors

def main(tx_id, num, tx_type, message, ids):

    # import the login info for psql from 'info.json'
    with open('info.json', 'r') as f:
        info = json.load(f)

    db_name = info['psql']['db_name']
    db_user = info['psql']['db_user']
    db_password = info['psql']['db_password']
    db_host = info['psql']['db_host']
    db_port = info['psql']['db_port']

    connection = create_connection(db_name, db_user, db_password, db_host, db_port)
    cursor = connection.cursor()
    try:
        # Define the values
        tx_denom = message['amount'][0]['denom']
        amount = message['amount'][0]['amount']
        message = json.dumps(message)
        comment = f'This is number {num} message in transaction {tx_id}'

        # Edit the query that will be loaded to the database
        query = """
        INSERT INTO cosmos_send_msg (tx_id, tx_type, from_address_id, to_address_id, tx_denom, amount, message_info, comment) VALUES (%s, %s, %s, %s, %s, %s, %s,%s);
        """

        values = (tx_id, tx_type, ids['from_address_id'], ids['to_address_id'], tx_denom, amount, message, comment)
        cursor.execute(query, values)

        connection.commit()
        connection.close()
    except KeyError:
        print(f'KeyError happens in type {tx_type}')
    except errors.UniqueViolation as e:
        pass

if __name__ == '__main__':
    main(tx_id, tx_type, message, ids)
