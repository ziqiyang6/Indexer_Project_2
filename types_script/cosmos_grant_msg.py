# !/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_grant_msg.py                                *
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
                INSERT INTO cosmos_grant_msg (tx_id, tx_type, send_address_id, receive_address_id, authorizationtype, expiration, max_tokens, authorization_type, msg, message_info) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING message_id;
                """

        # Define the values
        authorizationtype = message['grant']['authorization']['@type']
        expiration = message['grant']['expiration']

        # Condition 1: if there is more than two element in authorization, load like this
        if len(message['grant']['authorization']) > 2 :
            # If max tokens is NULL, make it as '', avoiding the error
            if message['grant']['authorization']['max_tokens'] == None:
                max_tokens = ''
            else:
                max_tokens = message['grant']['authorization']['max_tokens']
            authorization_type = message['grant']['authorization']['authorization_type']
            msg = ''
            message_info = json.dumps(message)
            values = (tx_id, tx_type, ids['granter_id'], ids['grantee_id'], authorizationtype, expiration, max_tokens, authorization_type, msg, message_info )
            cursor.execute(query, values)
            message_id = cursor.fetchone()[0]
            # In this condition, more info will be loaded to allow list table
            for address in message['grant']['authorization']['allow_list']['address']:

                cursor.execute('INSERT INTO cosmos_grant_allowlist (message_id, addresses) VALUES (%s, %s); ', (message_id, address))
        # Condition 2: If not , load like this
        else:
            authorization_type = ''

            msg = message['grant']['authorization']['msg']
            max_tokens = ''
            message_info = json.dumps(message)
            values = (tx_id, tx_type, ids['granter_id'], ids['grantee_id'], authorizationtype, expiration, max_tokens, authorization_type, msg, message_info  )
            cursor.execute(query, values)

        connection.commit()
        connection.close()
    except KeyError:
        print(f'KeyError happens in type {tx_type}')

if __name__ == '__main__':
    main(tx_id, tx_type, message, ids)
