#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: ibc_channelopentry_msg.py                                *
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
'version' column in query has been changed to 'version_num'.                              *                                                                                    *
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
        # Edit the query that will be loaded to the database
        query = """
                INSERT INTO ibc_channelopentry_msg (tx_id, tx_type, port_id, previous_channel_id, channel_state, channel_ordering, counterparty_port_id, counterparty_channel_id, connection_hops, version_num, counterparty_version, proof_init, proof_height_revision_number, proof_height_revision_height, signer, message_info) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Define the values
        port_id = message['port_id']
        previous_channel_id = message['previous_channel_id']
        channel_state = message['channel']['state']
        channel_ordering = message['channel']['ordering']
        counterparty_port_id = message['channel']['counterparty']['port_id']
        counterparty_channel_id = message['channel']['counterparty']['channel_id']
        connection_hops = message['channel']['connection_hops'][0]
        version = message['channel']['version']
        counterparty_version = message['counterparty_version']
        proof_init = message['proof_init']
        proof_height_revision_number = message['proof_height']['revision_number']
        proof_height_revision_height = message['proof_height']['revision_height']
        signer = message['signer']
        message = json.dumps(message)

        values = (tx_id, tx_type, port_id, previous_channel_id, channel_state, channel_ordering, counterparty_port_id, counterparty_channel_id, connection_hops, version, counterparty_version, proof_init, proof_height_revision_number, proof_height_revision_height, signer, message)
        cursor.execute(query, values)

        connection.commit()
        connection.close()

    except KeyError:
        print(f'KeyError happens in type {tx_type}')

if __name__ == '__main__':
    main(tx_id, tx_type, message)
