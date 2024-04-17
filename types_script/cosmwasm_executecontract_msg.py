#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmwasm_executecontract_msg.py                                *
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
                INSERT INTO cosmwasm_executecontract_msg (tx_id, tx_type, send_address_id, contracts, msg, tx_denom, amount, message_info) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Define the values
        contract = message['contract']
        message_info = json.dumps(message)

        # Condition 1: If key 'funds' contains any info, load like this
        if len(message['funds']) > 0 :
            tx_denom = message['funds'][0]['denom']
            amount = message['funds'][0]['amount']
            msg = message['msg']
            msg = list(msg)
            values = (tx_id, tx_type, ids['sender_id'], contract, msg, tx_denom, amount, message_info)
            cursor.execute(query, values)

        # Condition 2: If not, load this way
        else:
            tx_denom = ''
            amount = ''
            msg = message['msg']
            msg = list(msg)
            values = (tx_id, tx_type, ids['sender_id'], contract, msg, tx_denom, amount, message_info)
            cursor.execute(query, values)

        connection.commit()
        connection.close()

    except KeyError:
        print(f'KeyError happens in type {tx_type}')

if __name__ == '__main__':
    main(tx_id, tx_type, message, ids)
