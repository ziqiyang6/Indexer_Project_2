#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_unjail_msg.py                                *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                                     *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 5/31/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                   *
                                                                                    *
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
    message = json.dumps(message)
    comment = (
        f"This is number {message_no} message in number {transaction_no} transaction "
    )

    # Edit the query that will be loaded to the database
    query = """
        INSERT INTO cosmos_unjail_msg (tx_id, tx_type, validator_addr_id, message_info, comment) VALUES (%s, %s, %s, %s, %s);
        """

    values = (tx_id, tx_type, ids["validator_addr_id"], message, comment)
    return query, values
