"""**********************************************************************************
                                                                                    *
Project Name:ibc_core_channel_v1_msgchannelopenack.py                               *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json                                                                     *
                                                                                    *
Creater Name: Thomas Wang                                                           *
                                                                                    *
Published Date: 6/8/2024                                                            *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
                                                                                    *
**********************************************************************************"""  #    Scripts start below

import json
import sys
import os
import traceback
from psycopg2 import errors


def get_query(tx_id, message_no, transaction_no, tx_type, message):
    # Edit the query that will be loaded to the database
    query = """
                INSERT INTO ibc_core_channel_v1_msgchannelopenack(tx_id, tx_type, port_id, channel_id counterparty_channel_id signer, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

    # Define the values#
    port_id = message['port_id']
    channel_id = message['channel_id']
    counterparty_channel_id = message['counterparty_channel_id']
    signer = message['signer']
    message = json.dumps(message)
    comment = f'This is number {message_no} message in number {transaction_no} transaction '

    values = (
        tx_id,
        tx_type,
        port_id,
        channel_id,
        counterparty_channel_id,
        signer,
        message,
        comment,
    )
    return query, values
