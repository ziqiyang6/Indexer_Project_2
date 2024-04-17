#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: ibc_updateclient_msg.py                                                         *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                      *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 4/15/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
                                                                                    *
                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
from functions import create_connection
import json

def main(tx_id, tx_type, message):

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
        # Set the values that will be loaded to database
        client_id = message['client_id']
        client_message = json.dumps(message['client_message'])
        signer = message['signer']
        message = json.dumps(message)

        query = """
        INSERT INTO ibc_updateclient_msg (tx_id, tx_type, client_id, client_message, signer, message_info) VALUES (%s, %s, %s, %s, %s, %s);
        """

        values = (tx_id, tx_type, client_id, client_message, signer, message)
        cursor.execute(query, values)

        connection.commit()
        connection.close()

    except KeyError:
        print(f'KeyError happens in type {tx_type}')

if __name__ == '__main__':
    main(tx_id, tx_type, message)
