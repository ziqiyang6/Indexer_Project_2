# !/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_delegate_msg.py                                *
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
    # Define the values
    tx_denom = message["amount"]["denom"]
    amount = message["amount"]["amount"]
    message = json.dumps(message)
    comment = (
        f"This is number {message_no} message in number {transaction_no} transaction "
    )

    #  Edit the query that will be loaded to the database
    query = """
        INSERT INTO cosmos_delegate_msg (tx_id, tx_type, delegator_address_id, validator_address_id, tx_denom, amount, message_info, comment) VALUES (%s, %s, %s, %s, %s, %s,%s,%s);
        """

    values = (
        tx_id,
        tx_type,
        ids["delegator_address_id"],
        ids["validator_address_id"],
        tx_denom,
        amount,
        message,
        comment,
    )
    return query, values
