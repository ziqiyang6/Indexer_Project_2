#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmwasm_storecode_msg.py                                *
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
                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
from functions import create_connection
import json

def main(tx_id, tx_type, message, ids):

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
        # Edit the query that will be loaded to the database
        query = """
                INSERT INTO cosmwasm_storecode_msg (tx_id, tx_type, sender_address_id, wasm_byte_code, instantiate_permission, message_info) 
                VALUES (%s, %s, %s, %s, %s, %s);
                """

        # Define the values
        wasm_byte_code = message['wasm_byte_code']
        # If the value is NULL, make it as '', avoiding the error
        if message['instantiate_permission'] == None:
            instantiate_permission = []
        else:
            instantiate_permission = message['instantiate_permission']
        message = json.dumps(message)

        values = (tx_id, tx_type, ids['sender_id'], wasm_byte_code, instantiate_permission, message)
        cursor.execute(query, values)

        connection.commit()
        connection.close()
    except KeyError:
        print(f'KeyError happens in type {tx_type}')

if __name__ == '__main__':
    main(tx_id, tx_type, message, ids)
