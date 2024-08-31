# !/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: functions.py                                                          *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json  os    sys     requests  2.31.0      jsonschema   4.21.1           *
            time               psycopg2   2.9.9       hashlib         base64        *
            binascii                                                                *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 4/15/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
Version: 1.1                                                                        *
Function 'hash_to_hex' has been added to convert transaction string to hex hash     *
Function 'block_hash_base64_to_hex' has been added to convert base 64 block hash    *
to hex hash                                                                         *
hashlib, base64, and binascii, these three packages have been added                 *
All of them are included in original Python                                         *
                                                                                    *  
Version: 1.2                                                                        *
Function 'decode_tx' has been updated. The old url had been changed to new url      *
'https://terra-rest.publicnode.com/cosmos/tx/v1beta1/decode'                        *
                                                                                    *
Version: 1.3                                                                        *
Function 'new_type' has been created to store new message type if there is          *
**********************************************************************************'''

#    Functions start below
import importlib
import json
import os
from pathlib import Path
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import sys
import requests
import time
import psycopg2
from psycopg2 import OperationalError
import hashlib
import base64
import binascii
from datetime import datetime, timezone
import traceback
from psycopg2 import errors

MULTI_TX_TYPES = {"cosmos_grant_msg", "cosmos_multisend_msg"}


# //from terra_sdk.client.lcd import LCDClient
# from terra_sdk.core.tx import Tx #?/ trmintimport

def check_file(file_path,file_name):

    # Check if the file exists in the directory
    if os.path.isfile(file_path):
        pass
        # print(f'{file_name} does exist in {path_name}')
    else:
        print(
            f"{file_name} does not exist in {file_path}, or {file_name} is not a file",
            file=sys.stderr,
        )
        sys.exit(1)

        # Check if the file name is composed entirely of digits
    if file_name.isdigit():
        pass
        # print('This file is named by numbers')
    else:
        print(f"The file name {file_name} is not composed entirely of digits.", file=sys.stderr)
        sys.exit(2)

    # Check if it is a JSON file
    try:
        with open(file_path, 'r') as file:
            # print(f"{file_name} is a JSON file.")
            content = json.load(file)

    except json.JSONDecodeError:
        print(f"{file_name} is not a JSON file.", file=sys.stderr)
        file = open(file_path, "r")
        print(file)
        checkLine(file_path, file_name,len(file.readlines()) - 1)
        file.close()
        sys.exit(3)

    except ValueError as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        sys.exit(4)

    return content


def height_check(content,file_name):
    try:

        # Check if the file name equals the height
        height = content['block']['header']['height']
    except KeyError:
        print("There is not such key in the file", file=sys.stderr)
        sys.exit(5)
    except TypeError:
        print("The Type of value is not correct", file=sys.stderr)
        sys.exit(6)

    if height == file_name:
        # print(f'{file_name} is same as height.')
        pass
    else:
        print(f'Error: {file_name} does not same as height.', file=sys.stderr)
        sys.exit(7)

    # print(f'{file_name} is a valid JSON file and the name is same as the BLOCK HEIGHT'
    return height


def validate_json(content, file_name):
    schema = {
            "type": "object",
            "properties":{
                "block_id": {
                    "type": "object",
                    "properties": {
                        "hash": {
                            "type": "string",
                            "pattern": "^[A-Za-z0-9+/=]+$",
                            "minLength": 44,
                            "maxLength": 44
                        },
                        "part_set_header": {
                            "type": "object",
                            "properties": {
                                "total": {
                                "type": "integer"
                                },
                                "hash": {
                                    "type": "string",
                                    "pattern": "^[A-Za-z0-9+/=]+$",
                                    "minLength": 44,
                                    "maxLength": 44
                                },
                            },
                            "required": ["total","hash"]
                        },
                    },
                    "required": ["hash","part_set_header"]

                },
                "block": {
                    "type": "object",
                    "properties": {
                        "header": {
                            "type": "object",
                            "properties": {
                                "version": {
                                    "type": "object",
                                    "properties": {
                                        "block":{
                                            "type": "string",
                                            "pattern": "^\d+$"
                                        },
                                        "app": {
                                            "type": "string",
                                            "pattern": "^\d+$"
                                        },
                                    },
                                    "required": ["block","app"]
                                },
                                "chain_id": {
                                    "type": "string"
                                },
                                "height": {
                                    "type": "string",
                                    "pattern": "^\d+$"
                                },
                                "time": {
                                    "type": "string",
                                    "format": "date-time"
                                },
                                "last_block_id": {
                                    "type": "object",
                                    "properties": {
                                        "hash": {
                                            "type": "string",
                                            "pattern": "^[A-Za-z0-9+/=]+$",
                                            "minLength": 44,
                                            "maxLength": 44
                                        },
                                        "part_set_header": {
                                            "type": "object",
                                            "properties": {
                                                "total": {
                                                  "type": "integer"
                                                },
                                                "hash": {
                                                   "type": "string",
                                                    "pattern": "^[A-Za-z0-9+/=]+$",
                                                    "minLength": 44,
                                                    "maxLength": 44
                                                },
                                            },
                                            "required": ["total","hash"]
                                        },
                                    },
                                    "required": ["hash","part_set_header"]
                                },
                                "last_commit_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "data_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "validators_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "next_validators_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "consensus_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "app_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "last_results_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "evidence_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "proposer_address": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 28,
                                        "maxLength": 28
                                },
                            },
                            "required": ["version","chain_id","height", "time","last_block_id","last_commit_hash","data_hash","validators_hash","next_validators_hash","consensus_hash","app_hash","last_results_hash","evidence_hash","proposer_address"]
                        },
                        "data":{
                            "type": "object",
                            "properties": {
                                "txs": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                },
                            },
                            "required": ["txs"]
                        },
                        "evidence":{
                            "type": "object",
                            "properties": {
                                "evidence": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                },
                            },
                            "required": ["evidence"]
                        },
                        "last_commit":{
                            "type": "object",
                            "properties": {
                                "height": {
                                    "type": "string",
                                    "pattern": "^\d+$"
                                },
                                "round": {
                                    "type": "integer",
                                    "min": 0
                                },
                                "block_id":{
                                    "type": "object",
                                    "properties": {
                                        "hash":{
                                            "type": "string",
                                            "pattern": "^[A-Za-z0-9+/=]+$",
                                            "minLength": 44,
                                            "maxLength": 44
                                        },
                                        "part_set_header": {
                                            "type": "object",
                                            "properties": {
                                                "total": {
                                                    "type": "integer",
                                                    "min": 0
                                                },
                                                "hash":{
                                                    "type": "string",
                                                    "pattern": "^[A-Za-z0-9+/=]+$",
                                                    "minLength": 44,
                                                    "maxLength": 44
                                                }
                                            },
                                            "required": ["total","hash"]
                                        }
                                    },
                                    "required":["hash","part_set_header"]
                                },

                                "signatures": {
                                    "type": "array",
                                    "items": {
                                        "if" :{
                                            "properties": {
                                                "block_id_flag": {
                                                    "type": "string",
                                                    "pattern": "BLOCK_ID_FLAG_COMMIT"
                                                },
                                            },
                                        "then":{
                                                "properties": {
                                                 "block_id_flag": {
                                                       "type": "string"
                                                 },
                                                 "validator_address": {
                                                    "type": "string",
                                                    "pattern": "^[A-Za-z0-9+/=]+$"
                                                 },
                                                "timestamp": {
                                                    "type": "string",
                                                    "format": "date-time"
                                                },
                                                "signature": {
                                                    "type": "string",
                                                    "pattern": "^[A-Za-z0-9+/=]+$",
                                                    "minLength": 88,
                                                    "maxLength": 88
                                                }
                                            },
                                        },
                                        "else":{
                                            "properties": {
                                                 "block_id_flag": {
                                                       "type": "string"
                                                 },
                                                 "validator_address": {
                                                    "type": "string",
                                                    "pattern": "null"
                                                 },
                                                "timestamp": {
                                                    "type": "string",
                                                    "pattern": "0001-01-01T00:00:00Z"
                                                },
                                                "signature": {
                                                    "type": "string",
                                                    "pattern": "null"
                                                },
                                            },
                                        },
                                        "required": ["block_id_flag", "validator_address", "timestamp", "signature"]
                                        },
                                    }
                                }
                            },
                            "required": ["height","round","block_id","signatures"]
                        },
                    },
                    "required": ["header","data","evidence","last_commit"]
                },
                "sdk_block":{
                    "type": "object",
                    "properties": {
                        "header": {
                            "type": "object",
                            "properties": {
                                "version": {
                                    "type": "object",
                                    "properties": {
                                        "block":{
                                            "type": "string",
                                            "pattern": "^\d+$"
                                        },
                                        "app": {
                                            "type": "string",
                                            "pattern": "^\d+$"
                                        },
                                    },
                                    "required": ["block","app"]
                                },
                                "chain_id": {
                                    "type": "string"
                                },
                                "height": {
                                    "type": "string",
                                    "pattern": "^\d+$"
                                },
                                "time": {
                                    "type": "string",
                                    "format": "date-time"
                                },
                                "last_block_id": {
                                    "type": "object",
                                    "properties": {
                                        "hash": {
                                            "type": "string",
                                            "pattern": "^[A-Za-z0-9+/=]+$",
                                            "minLength": 44,
                                            "maxLength": 44
                                        },
                                        "part_set_header": {
                                            "type": "object",
                                            "properties": {
                                                "total": {
                                                  "type": "integer"
                                                },
                                                "hash": {
                                                   "type": "string",
                                                    "pattern": "^[A-Za-z0-9+/=]+$",
                                                    "minLength": 44,
                                                    "maxLength": 44
                                                },
                                            },
                                            "required": ["total","hash"]
                                        },
                                    },
                                    "required": ["hash","part_set_header"]
                                },
                                "last_commit_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "data_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "validators_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "next_validators_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "consensus_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "app_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "last_results_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "evidence_hash": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 44,
                                        "maxLength": 44
                                },
                                "proposer_address": {
                                        "type": "string",
                                        "pattern": "^[A-Za-z0-9+/=]+$",
                                        "minLength": 53,
                                        "maxLength": 53
                                },
                            },
                            "required": ["version","chain_id","height", "time","last_block_id","last_commit_hash","data_hash","validators_hash","next_validators_hash","consensus_hash","app_hash","last_results_hash","evidence_hash","proposer_address"]
                        },
                        "data":{
                            "type": "object",
                            "properties": {
                                "txs": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                },
                            },
                            "required": ["txs"]
                        },
                        "evidence":{
                            "type": "object",
                            "properties": {
                                "evidence": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                },
                            },
                            "required": ["evidence"]
                        },
                        "last_commit":{
                            "type": "object",
                            "properties": {
                                "height": {
                                    "type": "string",
                                    "pattern": "^\d+$"
                                },
                                "round": {
                                    "type": "integer",
                                    "min": 0
                                },
                                "block_id":{
                                    "type": "object",
                                    "properties": {
                                        "hash":{
                                            "type": "string",
                                            "pattern": "^[A-Za-z0-9+/=]+$"
                                        },
                                        "part_set_header": {
                                            "type": "object",
                                            "properties": {
                                                "total": {
                                                    "type": "integer",
                                                    "min": 0
                                                },
                                                "hash":{
                                                    "type": "string",
                                                    "pattern": "^[A-Za-z0-9+/=]+$"
                                                }
                                            },
                                            "required": ["total","hash"]
                                        }
                                    },
                                    "required":["hash","part_set_header"]
                                },

                                "signatures": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "if" :{
                                            "properties": {
                                                "block_id_flag": {
                                                    "type": "string",
                                                    "pattern": "BLOCK_ID_FLAG_COMMIT"
                                                },
                                            },
                                        "then":{
                                                "properties": {
                                                 "block_id_flag": {
                                                       "type": "string"
                                                 },
                                                 "validator_address": {
                                                    "type": "string",
                                                    "pattern": "^[A-Za-z0-9+/=]+$"
                                                 },
                                                "timestamp": {
                                                    "type": "string",
                                                    "format": "date-time"
                                                },
                                                "signature": {
                                                    "type": "string",
                                                    "pattern": "^[A-Za-z0-9+/=]+$",
                                                    "minLength": 88,
                                                    "maxLength": 88
                                                }
                                            },
                                        },
                                        "else":{
                                            "properties": {
                                                 "block_id_flag": {
                                                       "type": "string"
                                                 },
                                                 "validator_address": {
                                                    "type": "string",
                                                    "pattern": "null"
                                                 },
                                                "timestamp": {
                                                    "type": "string",
                                                    "pattern": "0001-01-01T00:00:00Z"
                                                },
                                                "signature": {
                                                    "type": "string",
                                                    "pattern": "null"
                                                },
                                            },
                                        },
                                        "required": ["block_id_flag", "validator_address", "timestamp", "signature"]
                                        },
                                    }

                                }
                            },
                            "required": ["height","round","block_id","signatures"]
                        },
                    },
                    "required": ["header","data","evidence","last_commit"]
                }
            },
            "required": ["block_id","block","sdk_block"]
    }

    try:
        validate(instance=content, schema=schema)
        # print(f'Content in {file_name} has been validated')
        return 1
    except ValidationError as ve:
        print(f"JSON data of {file_name} is invalid.", file=sys.stderr)
        print(ve, file=sys.stderr)
        print(traceback.format_exc())


def new_type(message, file_path, height, transaction_num, message_num):

        path = f'{file_path}/new_type.txt'

        # Check if the file exist
        if not os.path.isfile(path):
            print(f"File does not exist. Creating '{path}'...")
            try:
                # Use 'x' mode to create the file
                with open(path, 'x') as file:
                    print(f"File '{path}' created successfully.")
            except FileExistsError:
                pass

        # If and only if the type is unique, it will be stored.
        with open(path, 'a') as file:  # Use 'a' mode to append the content
            file.write(f"The message is the No. {message_num} message in No. {transaction_num} transaction  from block {height} \n")
            file.write(message + '\n' + '\n')


def decode_tx(tx, max_retries=10, retry_delay=2):
    """
    Decodes a transaction using an external API.

    Args:
        tx: The transaction to decode.
        max_retries: Maximum number of retries for the request.
        retry_delay: Time to wait between retries (in seconds).

    Returns:
        Decoded transaction if successful, None otherwise.
    """
    url_array = ["https://terra-rest.publicnode.com/", "https://api-terra-01.stakeflow.io", "https://terra-api.polkachu.com"]
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"tx_bytes": tx})
    retries = 0

    while retries < max_retries:
        try:
            full_url = url_array[retries] + "cosmos/tx/v1beta1/decode"
            response = requests.post(full_url, headers=headers, data=data, timeout=5)  # Adding a 5-second timeout
            if response.status_code == 200:
                # print(f"Successfully decoded transaction")
                return response.json()
            else:
                print(f"Error: Unable to decode transaction, server returned status code {response.status_code} using {full_url}", file=sys.stderr)
                if response.status_code in [400, 502, 503, 504]:  # Retry on certain status codes
                    time.sleep(retry_delay)
                    retries += 1
                else:
                    break  # Do not retry on other errors
        except requests.exceptions.RequestException as e:
            print(f"Network request error: {e} using {full_url}", file=sys.stderr)
            time.sleep(retry_delay)
            retries += 1

    return None


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        # print("Connection to PostgreSQL DB successful")#
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def load_block(connection, file_path, file_name):
    try:
        content = check_file(file_path, file_name)
        block_hash = content["block_id"]["hash"]
        block_hash_hex = block_hash_base64_to_hex(block_hash)
        chain_id = content["block"]["header"]["chain_id"]
        height = content["block"]["header"]["height"]
        tx_num = len(content["block"]["data"]["txs"])
        created_time = content["block"]["header"]["time"]
    except Exception as e:
        print(f"Error with loading block info in block " + file_name, file=sys.stderr)
        raise
    # Edit the query that will be loaded to the database
    query = """
    INSERT INTO blocks (block_hash, chain_id, height, tx_num, created_at) VALUES (%s, %s, %s, %s, %s);
    """

    values = (block_hash_hex, chain_id, height, tx_num, created_time)

    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
    except errors.UniqueViolation as e:
        connection.rollback()
    connection.commit()
    cursor.close()


def verify_block(connection, file_path, file_name):
    content = check_file(file_path, file_name)
    block_hash = content["block_id"]["hash"]
    block_hash_hex = block_hash_base64_to_hex(block_hash)
    chain_id = content["block"]["header"]["chain_id"]
    height = content["block"]["header"]["height"]
    tx_num = str(len(content["block"]["data"]["txs"]))
    created_time = content["block"]["header"]["time"]

    cursor = connection.cursor()

    # check block information was inserted into database correctly
    # get the block hash, chain id, height, tx number, and created time from database
    query = """
    SELECT block_hash, chain_id, height, tx_num, created_at FROM blocks WHERE block_hash = %s;
    """

    values = (block_hash_hex,)

    try:
        cursor.execute(query, values)
        result = cursor.fetchall()
        cursor.close()
        # check there should only be one row
        if result is None or len(result) != 1:
            # print to stderr
            print("There should be only one row", file=sys.stderr)

        result = result[0]

        # check the block information is correct
        if result[1] != chain_id or result[2] != height or result[3] != tx_num:
            if result[1] != chain_id:
                print(
                    "Chain id is not correct, found",
                    result[1],
                    "expected",
                    chain_id,
                    file=sys.stderr,
                )
            if result[2] != height:
                print(
                    "Height is not correct, found",
                    result[2],
                    "expected",
                    height,
                    file=sys.stderr,
                )
            if result[3] != tx_num:
                print(
                    "Tx number is not correct, found",
                    result[3],
                    "expected",
                    tx_num,
                    file=sys.stderr,
                )
        # print(created_time, file=sys.stderr)
        # print(len(created_time), file=sys.stderr)
        created_time = time_parse(created_time)
        # convert the database time to utc
        database_time = result[4].astimezone(timezone.utc).replace(microsecond=0)
        # check that the created time is correct to the second, ignore the milliseconds
        if created_time != database_time:
            print(
                "Created time is not correct, found",
                database_time,
                "expected",
                created_time,
                file=sys.stderr,
            )

    except errors.UniqueViolation as e:
        connection.rollback()

    connection.commit()
    cursor.close()


def is_valid_file(file_path, file_name):
    result = check_file(file_path, file_name)

    # Check if this file passes JSON Schema test. 1 is the specific case that passes.
    if validate_json(result, file_name) == 1:
        return True, result
    else:
        foundError = checkLine(file_name, 1)
        if foundError >= 0:
            try:
                with open(file_name, "r") as fr:
                    # reading line by line
                    lines = fr.readlines()

                    # pointer for position
                    ptr = 1

                    # opening in writing mode
                    with open(file_name, "w") as fw:
                        for line in lines:

                            # we want to remove 5th line
                            if ptr != foundError:
                                fw.write(line)
                            ptr += 1
                print("Deleted", file=sys.stderr)
            except:
                print("Error in file", file=sys.stderr)
        return False, None


def get_num_txs(content):
    count = len(content["block"]["data"]["txs"])
    return count


def address_load(connection, address, file_name):
    cursor = connection.cursor()
    # Define the values
    comment = ""
    created_time = datetime.now()
    updated_time = created_time

    # Find the index of number 1 in the string
    index_of_1 = address.find("1")
    # Count the length after 1
    substring_after_1 = address[index_of_1 + 1 :]
    length_after_1 = len(substring_after_1)
    # print(length_after_1, file=sys.stderr)
    # If the string contains 'valoper' string, this is a validator address
    validator = "valoper"
    if validator in address:
        address_type = "validator"
    # If the length larger than 38, this is a contract address
    elif length_after_1 >= 38:
        address_type = "contract"
    # If the length after 1 equals 38, this is a user address
    elif length_after_1 == 38:
        address_type = "user"
    elif len(address) == 0:
        address_type = "blank"
    # If the address does not belong to three types above, it will be an unknown type
    else:
        address_type = "Unknown"
        print(
            f"The type of address could not be detected, check address"
            + address
            + " in block "
            + file_name,
            file=sys.stderr,
        )

    query = """
    INSERT INTO address (address_type, addresses, comment, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)
    RETURNING address_id;
    
    """

    # Load the values
    values = (address_type, address, comment, created_time, updated_time)
    try:
        cursor.execute(query, values)
        address_id = cursor.fetchone()[0]

    except errors.UniqueViolation as e:
        connection.rollback()
        search_query = f"SELECT address_id FROM address WHERE addresses = '{address}'"
        cursor.execute(search_query)
        address_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    return address_id


def load_tx(connection, file_path, file_name, num):
    cursor = connection.cursor()

    # Set the path of file
    output_path = os.getenv("txt")
    cwd = os.getcwd()

    # Set the values that will be loaded to database
    content = check_file(file_path, file_name)
    # decoded_response = decode_tx(content['block']['data']['txs'][int(num)])
    try:
        transaction_string = content["block"]["data"]["txs"][int(num)]
        decoded_response = decode_tx(transaction_string)
        if decoded_response == None:
            print(f"failed to decode transaction in block {file_name}", file=sys.stderr)
            exit()
        tx_hash = hash_to_hex(transaction_string)
        chain_id = content["block"]["header"]["chain_id"]
        height = content["block"]["header"]["height"]
        search_query = f"SELECT block_id FROM blocks WHERE height = '{height}'"  # Search the block hash from the block
        cursor.execute(search_query)
        result = cursor.fetchall()
        block_id = result[0][0]
        memo = decoded_response["tx"]["body"]["memo"]

        if len(decoded_response["tx"]["auth_info"]["fee"]["amount"]) != 0:
            # print("run")
            fee_denom = decoded_response["tx"]["auth_info"]["fee"]["amount"][0]["denom"]
            fee_amount = decoded_response["tx"]["auth_info"]["fee"]["amount"][0][
                "amount"
            ]
        else:
            fee_denom = ""
            fee_amount = 0
        gas_limit = decoded_response["tx"]["auth_info"]["fee"]["gas_limit"]
        created_time = content["block"]["header"]["time"]
        order = int(num) + 1
        comment = f"This is number {order} transaction in BLOCK {height}"
        tx_info = json.dumps(decoded_response)
    except Exception as e:
        print(f"Error with loading block info in block " + file_name, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        raise

    # Edit the query that will be loaded to the database
    query = """
    INSERT INTO transactions (block_id, tx_hash, chain_id, height, memo, fee_denom, fee_amount, gas_limit, created_at, tx_info, comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING tx_id;
    """
    values = (
        block_id,
        tx_hash,
        chain_id,
        height,
        memo,
        fee_denom,
        fee_amount,
        gas_limit,
        created_time,
        tx_info,
        comment,
    )

    try:
        cursor.execute(query, values)
        tx_id = cursor.fetchone()[0]
    except errors.UniqueViolation as e:
        connection.rollback()
        search_query = f"SELECT tx_id FROM transactions WHERE block_id = '{block_id}'"
        cursor.execute(search_query)
        tx_id = cursor.fetchone()[0]

    # connection.commit()

    # Message loading
    # Read the type.json file
    with open("type.json", "r") as f:
        type_json = json.load(f)

    # Use FOR LOOP to load every message in the transaction
    i = 1
    for message in decoded_response["tx"]["body"]["messages"]:

        # Define the type of message to find the corresponding python script

        type = message["@type"]

        try:
            table_type = type_json[type]
        except KeyError:
            print(
                f"Error with loading block info in block " + file_name, file=sys.stderr
            )
            print(traceback.format_exc(), file=sys.stderr)
            new_type(str(message), output_path, height, order, i)
            continue

        ids = {}
        for key in message:
            # Use keywords to catch address keys
            if (
                "send" in key
                or "receiver" in key
                or "addr" in key
                or "grante" in key
                or "admin" in key
                or "voter" in key
            ):
                # Define the address value and run the address_load script to load address
                address = message[key]
                ids[f"{key}_id"] = address_load(connection, address, file_name)

        # Load the type and height to type table
        try:
            cursor.execute(
                "INSERT INTO type (type, height) VALUES (%s, %s);", (type, height)
            )
        except errors.UniqueViolation as e:
            connection.rollback()

        # connection.commit()

        try:
            # Go to the diectory that contains the scripts
            module_path = Path(f"{cwd}/types_script")
            expanded_script_path = os.path.expanduser(module_path)
            sys.path.append(expanded_script_path)

            # Import the corresponding script
            table = importlib.import_module(table_type)
            # If the message contains the address, address_id will be added
            if table_type in MULTI_TX_TYPES:
                # print("Multi Type")
                if len(ids) > 0:
                    table.main(
                        connection, file_name, tx_id, i, order, type, message, ids
                    )
                else:
                    table.main(connection, file_name, tx_id, i, order, type, message)
            else:
                query, values = None, None
                if len(ids) > 0:
                    query, values = table.get_query(tx_id, i, order, type, message, ids)
                # If not, address_id will not
                else:
                    query, values = table.get_query(tx_id, i, order, type, message)
                cursor.execute(query, values)
        except KeyError:
            connection.rollback()
            print(f"KeyError happened in block {file_name}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
        except errors.UniqueViolation as e:
            connection.rollback()
        except AttributeError:
            print(
                f"Script {table_type} does not have a main function, error caused in block {file_name}",
                file=sys.stderr,
            )
        except ImportError:
            print(
                f"Script {table_type} could not be found, error caused in block {file_name}",
                file=sys.stderr,
            )
        i += 1

    connection.commit()

    cursor.close()


def verify_tx(connection, file_path, file_name, content, num):

    block_hash = content["block_id"]["hash"]
    block_hash_hex = block_hash_base64_to_hex(block_hash)
    chain_id = content["block"]["header"]["chain_id"]
    height = content["block"]["header"]["height"]
    tx_num = str(len(content["block"]["data"]["txs"]))
    created_time = content["block"]["header"]["time"]

    transaction_string = content["block"]["data"]["txs"][int(num)]
    decoded_response = decode_tx(transaction_string)
    # print(decoded_response)
    tx_hash = hash_to_hex(transaction_string)
    order = int(num) + 1
    loadedCorrectly = True
    cursor = connection.cursor()
    search_query = f"SELECT block_id FROM blocks WHERE height = '{height}'"  # Search the block hash from the block
    cursor.execute(search_query)
    result = cursor.fetchall()
    ##########block_id =

    if len(decoded_response["tx"]["auth_info"]["fee"]["amount"]) != 0:
        fee_denom = decoded_response["tx"]["auth_info"]["fee"]["amount"][0]["denom"]
        fee_amount = decoded_response["tx"]["auth_info"]["fee"]["amount"][0]["amount"]
    else:
        fee_denom = "0"
        fee_amount = "0"

    trans_values = {
        "block_id": result[0][0],
        "tx_hash": hash_to_hex(transaction_string),
        "chain_id": content["block"]["header"]["chain_id"],
        "height": content["block"]["header"]["height"],
        "memo": decoded_response["tx"]["body"]["memo"],
        "fee_denom": fee_denom,
        "fee_amount": fee_amount,
        "gas_limit": decoded_response["tx"]["auth_info"]["fee"]["gas_limit"],
        "created_at": content["block"]["header"]["time"],
        "tx_info": json.dumps(decoded_response),
        "comment": f"This is number {order} transaction in BLOCK {height}",
    }
    # print(decoded_response)
    try:
        query = f"SELECT block_id, tx_hash, chain_id, height, memo, fee_denom, fee_amount, gas_limit, created_at, tx_info, comment FROM transactions WHERE height = %s AND tx_hash = %s"
        cursor.execute(query, (height, tx_hash))
        row = cursor.fetchall()

        if row is None:

            print(row, file=sys.stderr)
            print(
                "There should be only one row in block "
                + file_name
                + " at transaction "
                + num
                + ", found",
                len(row),
                "rows",
                file=sys.stderr,
            )
            # break
            # print("error")
        else:
            row = row[0]
            colnames = [desc[0] for desc in cursor.description]
            row_dict = dict(zip(colnames, row))
            for col in trans_values:
                # print(trans_values[col])
                # print(row_dict[col])_tx
                db_info = str(row_dict[col])
                block_info = trans_values[col]

                if col == "created_at":
                    # print(block_info)
                    # print(db_info)
                    # print(len(trans_values))
                    formatted_dt = time_parse(trans_values[col])
                    block_info = formatted_dt
                    db_info = (
                        row_dict[col].astimezone(timezone.utc).replace(microsecond=0)
                    )

                if col == "tx_info":
                    try:
                        db_tx_info = json.dumps(row_dict[col])
                        db_info = json.loads(db_tx_info)
                        block_info = json.loads(trans_values[col])
                    except json.JSONDecodeError as e:
                        print("JSONDecodeError:", e)
                        print(f"Error in block " + file_name)

                if block_info != db_info:
                    print(
                        f"Error in block "
                        + file_name
                        + " at transaction "
                        + num
                        + " in column "
                        + col
                        + " found\n",
                        "Expected: " + str(block_info) + "\n",
                        "Found: " + str(db_info) + "\n",
                        file=sys.stderr,
                    )

    except errors.UniqueViolation as e:
        connection.rollback()

    connection.commit()
    cursor.close()


def hash_to_hex(data: str) -> str:
    try:
        # Convert data from base64 to bytes
        data_bytes = base64.b64decode(data)
        # Calculate SHA-256 hash
        sha256_hash = hashlib.sha256(data_bytes).hexdigest()
        # Convert hash to uppercase
        return sha256_hash.upper()
    except Exception as e:
        print(f"Error while hashing: {e}")
        return None

def block_hash_base64_to_hex(hash: str) -> str:
    try:
        # Convert data from base64 to bytes
        data_bytes = base64.b64decode(hash)
        # Convert SHA-256 hash
        hex_str = binascii.hexlify(data_bytes).decode('utf-8')
        # Convert hash to uppercase
        return hex_str.upper()
    except Exception as e:
        print(f"Error while hashing: {e}")
        return None
def checkLine(file_path, file_name, N):
       try:
            print("ran", file=sys.stderr)
            with open(file_path, 'r') as fr:
                # reading line by line
                lines = fr.readlines()
                if(N >= len(lines) or N == 0):
                    print(f"Error: Line number does not exist", file=sys.stderr)
                else:
                    if lines[N - 1].strip() != '':
                        foundError = N
                    else:
                        foundError = -1
                    # pointer for position
                    ptr = 1
                
                    # opening in writing mode
                    if foundError != -1:
                        with open(file_path, 'w') as fw:
                            for line in lines:
                            
                                # we want to remove 5th line
                                if ptr != foundError:
                                    fw.write(line)
                                ptr += 1
                        print(foundError, sys.stderr)
            print("Deleted", file=sys.stderr)
            
            check_file(file_path, file_name)
       except:
            print("Oops! something error", sys.stderr)
            print(traceback.format_exc())


def time_parse(time_string):
    timestamp_truncated = time_string[:19] # ignore the milliseconds
    created_time = (
        datetime.strptime(timestamp_truncated, "%Y-%m-%dT%H:%M:%S")
        .replace(tzinfo=timezone.utc)
        .replace(microsecond=0)
    )
    return created_time


def time_parse_old(time_string):
    time_list = list(time_string)
    #print(time_string)
    if len(time_string) == 30:
        milisecond_str = ""
        microsecond_str = ""
        for item in time_list[20: 26]:
            milisecond_str = milisecond_str + item
            for item in time_list[26:-2]:
                microsecond_str = microsecond_str + item
        rounded_mili = milisecond_str + "." + microsecond_str
        #print(rounded_mili)
        rounded_mili = round(float(rounded_mili))
        rounded_mili = str(rounded_mili).zfill(len(milisecond_str))
                    
                    
                    
        time_list = "".join(time_list[:20])
        time_list = time_list + rounded_mili
                    
                
        dt = datetime.strptime(time_list, "%Y-%m-%dT%H:%M:%S.%f")                
        formatted_dt =  dt.strftime("%Y-%m-%d %H:%M:%S.%f") + "+00:00"
    else:
        parsed_time_string = time_string.replace("Z", "")
        dt = datetime.strptime(parsed_time_string, "%Y-%m-%dT%H:%M:%S.%f")
        formatted_dt =  dt.strftime("%Y-%m-%d %H:%M:%S.%f") + "+00:00"

    return formatted_dt      
