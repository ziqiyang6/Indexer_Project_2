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
from functions import create_connection
import json
import sys
import os
import traceback
from psycopg2 import errors


def get_query(tx_id, message_no, transaction_no, tx_type, message, ids):
    query = """
                INSERT INTO ibc_transfer_msg (tx_id, tx_type, sender_address_id, receiver_address_id, source_port, source_channel, token_denom, token_amount, timeout_height_revision_num, timeout_height_revision_height, timeout_timestamp, memo, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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
    comment = f'This is number {message_no} message in number {transaction_no} transaction '

    values = (
        tx_id,
        tx_type,
        ids["sender_id"],
        ids["receiver_id"],
        source_port,
        source_channel,
        token_denom,
        token_amount,
        timeout_height_revision_num,
        timeout_height_revision_height,
        timeout_timestamp,
        memo,
        message,
        comment,
    )
    return query, values
