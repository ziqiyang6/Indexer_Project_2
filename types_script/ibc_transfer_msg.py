#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: ibc_transfer_msg.py                                *
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

    try:

        connection = create_connection(db_name, db_user, db_password, db_host, db_port)
        cursor = connection.cursor()

        query = """
                INSERT INTO ibc_transfer_msg (tx_id, tx_type, sender_address_id, receiver_address_id, source_port, source_channel, token_denom, token_amount, timeout_height_revision_num, timeout_height_revision_height, timeout_timestamp, memo, message_info) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Set the values that will be loaded to database
        source_port = message['source_port']
        source_channel = message['source_channel']
        token_denom = message['token']['denom']
        token_amount = message['token']['amount']
        timeout_height_revision_num = message['timeout_height']['revision_number']
        timeout_height_revision_height = message['timeout_height']['revision_height']
        timeout_timestamp = message['timeout_timestamp']
        memo = message['memo']
        message = json.dumps(message)

        values = (tx_id, tx_type, ids['sender_id'], ids['receiver_id'], source_port, source_channel, token_denom, token_amount, timeout_height_revision_num, timeout_height_revision_height, timeout_timestamp, memo, message)
        cursor.execute(query, values)

        connection.commit()
        connection.close()

    except KeyError:
        print(f'KeyError happens in type {tx_type}')

if __name__ == '__main__':
    main(tx_id, tx_type, message, ids)
