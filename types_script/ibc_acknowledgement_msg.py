#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: ibv_acknowledegment_msg.py                                *
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
'data' column in query has been changed to 'data_msg'.                              *
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
                INSERT INTO ibc_acknowledgement_msg (tx_id, tx_type, sequence_num, source_port, source_channel, destination_port, destination_channel, data_msg, timeout_height_revision_number, timeout_height_revision_height, timeout_timestamp, acknowledgement, proof_acked, proof_height_revision_number, proof_height_revision_height, signer, message_info) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Define the values
        sequence =  message['packet']['sequence']
        source_port = message['packet']['source_port']
        source_channel = message['packet']['source_channel']
        destination_port = message['packet']['destination_port']
        destination_channel = message['packet']['destination_channel']
        data = message['packet']['data']
        timeout_height_revision_num = message['packet']['timeout_height']['revision_number']
        timeout_height_revision_height = message['packet']['timeout_height']['revision_height']
        timeout_timestamp = message['packet']['timeout_timestamp']
        acknowledgement = message['acknowledgement']
        proof_acked = message['proof_acked']
        proof_height_revision_number = message['proof_height']['revision_number']
        proof_height_revision_height = message['proof_height']['revision_height']
        signer = message['signer']
        message = json.dumps(message)

        values = (tx_id, tx_type, sequence, source_port, source_channel, destination_port, destination_channel, data, timeout_height_revision_num, timeout_height_revision_height, timeout_timestamp, acknowledgement, proof_acked, proof_height_revision_number, proof_height_revision_height, signer, message)
        cursor.execute(query, values)

        connection.commit()
        connection.close()

    except KeyError:
        print(f'KeyError happens in type {tx_type}')


if __name__ == '__main__':
    main(tx_id, tx_type, message)
