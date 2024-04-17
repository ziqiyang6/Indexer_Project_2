# !/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_editvalidator_msg.py                                *
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
                INSERT INTO cosmos_editvalidator_msg (tx_id, tx_type, validator_address_id, description_moniker, description_identity, description_website, description_security_contact, description_details, commission_rate, min_self_delegation, message_info) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        # Define the values
        description_moniker = message['description']['moniker']
        description_identity = message['description']['identity']
        description_website = message['description']['website']
        description_security_contact = message['description']['security_contact']
        description_details = message['description']['details']
        commission_rate = message['commission_rate']

        # If self delegation is NULL, make it as ''
        if message['min_self_delegation'] == None:
            min_self_delegation = ''
        else:
            min_self_delegation = message['min_self_delegation']
        message = json.dumps(message)

        values = (tx_id, tx_type, ids['validator_address_id'], description_moniker, description_identity, description_website, description_security_contact, description_details, commission_rate, min_self_delegation, message)
        cursor.execute(query, values)

        connection.commit()
        connection.close()
    except KeyError:
        print(f'KeyError happens in type {tx_type}')

if __name__ == '__main__':
    main(tx_id, tx_type, message, ids)
