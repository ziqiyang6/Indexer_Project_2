#    Scripts start below
import json
import sys
import os
import traceback
from psycopg2 import errors


def get_query(tx_id, message_no, transaction_no, tx_type, message):

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

    values = (
        tx_id,
        tx_type,
        client_type,
        client_chain_id,
        client_trust_level_num,
        client_trust_level_denom,
        latest_height_revision_num,
        latest_height_revision_height,
        frozen_height_revision_number,
        frozen_height_revision_height,
        signer,
        message,
        comment,
    )
    return query, values
