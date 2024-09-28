#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: ibc_timeout_msg.py                                *
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
'data' column in query has been changed to 'data_msg'.                              *                                                                                    *
                                                                                    *
Version: 1.2                                                                        *
For 'cursor.execute' command, there is 'try' and 'except' to catch UniqueViolation  *
And if UniqueViolation happens, there will be search query to search needed value   *
New package: psycopg2 now applies on this script                                    *
New column 'comment' for transaction table has been added                           *                                                                                    *
                                                                                    *
Version: 1.3                                                                        *
Comment has been updated. tx_id has been replaced to transaction order.             *
KeyError output now can be printed into error log instead of output log             *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
import json
import sys
import os
import traceback
from psycopg2 import errors


def get_query(tx_id, message_no, transaction_no, tx_type, message):
    query = """
                INSERT INTO ibc_timeout_msg (tx_id, tx_type, sequence_num, source_port, source_channel, destination_port, destination_channel, data_msg, timeout_height_revision_number, timeout_height_revision_height, timeout_timestamp, proof_unreceived, proof_height_revision_number, proof_height_revision_height, next_seq_recv, signer, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
    sequence =  message['packet']['sequence']
    source_port = message['packet']['source_port']
    source_channel = message['packet']['source_channel']
    destination_port = message['packet']['destination_port']
    destination_channel = message['packet']['destination_channel']
    data = message['packet']['data']
    timeout_height_revision_num = message['packet']['timeout_height']['revision_number']
    timeout_height_revision_height = message['packet']['timeout_height']['revision_height']
    timeout_timestamp = message['packet']['timeout_timestamp']
    proof_unreceived = message['proof_unreceived']
    proof_height_revision_number = message['proof_height']['revision_number']
    proof_height_revision_height = message['proof_height']['revision_height']
    next_sequence_recv = message['next_sequence_recv']
    signer = message['signer']
    message = json.dumps(message)
    comment = f'This is number {message_no} message in number {transaction_no} transaction '

    values = (
        tx_id,
        tx_type,
        sequence,
        source_port,
        source_channel,
        destination_port,
        destination_channel,
        data,
        timeout_height_revision_num,
        timeout_height_revision_height,
        timeout_timestamp,
        proof_unreceived,
        proof_height_revision_number,
        proof_height_revision_height,
        next_sequence_recv,
        signer,
        message,
        comment,
    )
    return query, values
