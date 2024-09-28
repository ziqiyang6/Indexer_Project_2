'''**********************************************************************************
                                                                                    *
Project Name: ibc_core_channel_v1_msgchannelopeninit.py                             *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json, psycopg2                                                           *
                                                                                    *
Creater Name: Thomas Wang                                                           *
                                                                                    *
Published Date: 6/8/2024                                                            *
                                                                                    *
Version: 1.0                                                                        *
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


def get_query(tx_id, message_no, transaction_no, tx_type, message):
    # Edit the query that will be loaded to the database
    query = """
                INSERT INTO ibc_core_channel_v1_msgchannelopeninit (tx_id, tx_type, port_id, channel, channel_state, channel_ordering, counterparty_port_id, counterparty_channel_id, connection_hops, version_num, signer, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

    # Define the values#
    port_id = message['port_id']
    channel = message['channel']
    channel_state = message['channel']['state']
    channel_ordering = message['channel']['ordering']
    counterparty_port_id = message['channel']['counterparty']['port_id']
    counterparty_channel_id = message['channel']['counterparty']['channel_id']
    connection_hops = message['channel']['connection_hops'][0]
    version = message['channel']['version']
    signer = message['signer']
    message = json.dumps(message)
    comment = f'This is number {message_no} message in number {transaction_no} transaction '

    values = (
        tx_id,
        tx_type,
        port_id,
        channel,
        channel_state,
        channel_ordering,
        counterparty_port_id,
        counterparty_channel_id,
        connection_hops,
        version,
        signer,
        message,
        comment,
    )
    return query, values
