#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: cosmos_vote_msg.py                                                    *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json   sys                                                                  *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 5/27/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
import json
from psycopg2 import errors
import sys
import os
import traceback


def get_query(tx_id, message_no, transaction_no, tx_type, message, ids):
    # Define the values
    proposal_id = message['proposal_id']
    option = message['option']
    if message['metadata'] == None:
        metadata = ''
    else:
        metadata = message['metadata']
    message = json.dumps(message)
    comment = f'This is number {message_no} message in number {transaction_no} transaction '

    # Edit the query that will be loaded to the database
    query = """
        INSERT INTO cosmos_vote_msg (tx_id, tx_type, proposal_id, voter_address_id, options, metadata, message_info, comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

    values = (
        tx_id,
        tx_type,
        proposal_id,
        ids["voter_id"],
        option,
        metadata,
        message,
        comment,
    )
    return query, values
