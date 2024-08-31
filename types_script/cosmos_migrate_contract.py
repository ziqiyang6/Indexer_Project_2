#    Scripts start below
import json
import sys
import os
import traceback
from psycopg2 import errors


def get_query(tx_id, message_no, transaction_no, tx_type, message, ids):
    # Edit the query that will be loaded to the database
    query = """
                INSERT INTO cosmwasm_migratecontract_msg (tx_id, tx_type, send_address_id, contracts, code_id, msg, message_info, comment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
    contract = message['contract']
    message_info = json.dumps(message)
    comment = f'This is number {message_no} message in number {transaction_no} transaction '

    code_id = message["code_id"]
    msg = list(message["msg"]["with_update"])
    # public_keys_info = [{"type": pk["@type"], "key": pk["key"]} for pk in data["signer_infos"][0]["public_key"]["public_keys"]]
    # public_keys = [pk["key"] for pk in ["signer_infos"][0]["public_key"]["public_keys"]]
    # signer_infos = message['auth_info']['signer_infos']['public_key']
    values = (
        tx_id,
        tx_type,
        ids["sender_id"],
        contract,
        code_id,
        msg,
        message_info,
        comment,
    )
    return query, values
