#    Scripts start below
import json
import sys
import os
import traceback
from psycopg2 import errors


def get_query(tx_id, message_no, transaction_no, tx_type, message, ids):
    # Edit the query that will be loaded to the database
    query = """
                INSERT INTO cosmwasm_msg_instantiate_contract2 (tx_id, tx_type, send_address_id, admin_address_id, code_id, label, msg_swap_venues,funds, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

    # Define the values
    sender = ids["sender_id"]
    admin = ids["admin_id"]
    if sender != ids["sender_id"]:
        sender = message["sender"]  # s
    if admin != ids["admin_id"]:
        admin = message["admin"]
    code_id = message["code_id"]
    label = message["label"]
    msg = list(message["msg"])
    funds = message["funds"]
    message = json.dumps(message)
    comment = (
        f"This is number {message_no} message in number {transaction_no} transaction "
    )

    values = (
        tx_id,
        tx_type,
        sender,
        admin,
        code_id,
        label,
        msg,
        funds,
        message,
        comment,
    )
    return query, values
