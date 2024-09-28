#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: ibc_channelopenconfirm_msg.py                                *
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
For 'cursor.execute' command, there is 'try' and 'except' to catch UniqueViolation  *
And if UniqueViolation happens, there will be search query to search needed value   *
New package: psycopg2 now applies on this script                                    *
New column 'comment' for transaction table has been added                           *                                                                                    *
                                                                                    *
Version: 1.2                                                                        *
Comment has been updated. tx_id has been replaced to transaction order.             *
KeyError output now can be printed into error log instead of output log             *                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
import json
import sys
import os
import traceback
from psycopg2 import errors


def get_query(tx_id, message_no, transaction_no, tx_type, message):
    # Edit the query that will be loaded to the database
    query = """
                INSERT INTO ibc_channelopenconfirm_msg (tx_id, tx_type, port_id, channel_id, proof_acked, proof_height_revision_number, proof_height_revision_height, signer, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

    # Define the values
    port_id = message['port_id']
    channel_id = message['channel_id']
    proof_ack = message['proof_ack']
    proof_height_revision_number = message['proof_height']['revision_number']
    proof_height_revision_height = message['proof_height']['revision_height']
    signer = message['signer']
    message = json.dumps(message)
    comment = f'This is number {message_no} message in number {transaction_no} transaction '

    values = (
        tx_id,
        tx_type,
        port_id,
        channel_id,
        proof_ack,
        proof_height_revision_number,
        proof_height_revision_height,
        signer,
        message,
        comment,
    )
    return query, values
