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


def get_query(tx_id, message_no, transaction_no, tx_type, message, ids):
    # Edit the query that will be loaded to the database
    query = """
                INSERT INTO cosmwasm_executecontract_msg (tx_id, tx_type, send_address_id, contracts, msg, tx_denom, amount, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

    # Define the values
    contract = message['contract']
    message_info = json.dumps(message)
    comment = f'This is number {message_no} message in number {transaction_no} transaction '

    # Condition 1: If key 'funds' contains any info, load like this
    if len(message["funds"]) > 0:
        tx_denom = message["funds"][0]["denom"]
        amount = message["funds"][0]["amount"]
        msg = message["msg"]
        msg = list(msg)
        values = (
            tx_id,
            tx_type,
            ids["sender_id"],
            contract,
            msg,
            tx_denom,
            amount,
            message_info,
            comment,
        )

    # Condition 2: If not, load this way
    else:
        tx_denom = ""
        amount = ""
        msg = message["msg"]
        msg = list(msg)
        values = (
            tx_id,
            tx_type,
            ids["sender_id"],
            contract,
            msg,
            tx_denom,
            amount,
            message_info,
            comment,
        )

    return query, values
