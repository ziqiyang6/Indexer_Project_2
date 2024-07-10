
#    Scripts start below
from functions import create_connection
import json
import sys
import os
import traceback
from psycopg2 import errors

def main(tx_id, message_no, transaction_no, tx_type, message):

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
    file_name = os.getenv('FILE_NAME')
    try:
        # Edit the query that will be loaded to the database
        query = """
                INSERT INTO ibc_createclient_msg (tx_id, tx_type, client_type, client_chain_id, client_trust_level_num, client_trust_level_denom, latest_height_revision_num, latest_height_revision_height, frozen_height_revision_number, frozen_height_revision_height, signer, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
        # Define the values
        client_type = message['client_state']['@type']
        client_chain_id = message['client_state']['chain_id']
        client_trust_level_num = message['client_state']['trust_level']['numerator']
        client_trust_level_denom = message['client_state']['trust_level']['denominator']
        latest_height_revision_num = message['client_state']['latest_height']['revision_number']
        latest_height_revision_height = message['client_state']['latest_height']['revision_height']
        frozen_height_revision_number = message['client_state']['frozen_height']['revision_number']
        frozen_height_revision_height = message['client_state']['frozen_height']['revision_height']
        signer = message['signer']
        message = json.dumps(message)
        comment = f'This is number {message_no} message in number {transaction_no} transaction '

        values = (tx_id, tx_type, client_type, client_chain_id, client_trust_level_num, client_trust_level_denom, latest_height_revision_num, latest_height_revision_height, frozen_height_revision_number, frozen_height_revision_height, signer, message, comment)
        cursor.execute(query, values)

        connection.commit()
        connection.close()

    except KeyError:

        print(f'KeyError happens in type {tx_type} in block {file_name}', file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
    except errors.UniqueViolation as e:
        pass

if __name__ == '__main__':
    main(tx_id, message_no, transaction_no, tx_type, message)
