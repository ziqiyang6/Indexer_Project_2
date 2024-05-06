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
'https://lcd-terra.tfl.foundation/cosmos/tx/v1beta1/decode'                         *
**********************************************************************************'''

#    Functions start below
import json
import os
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


def check_file(file_path,file_name):

    # Check if the file exists in the directory
    if os.path.isfile(file_path):
        pass
        # print(f'{file_name} does exist in {path_name}')
    else:
        print(f'{file_name} does exist in {file_path}, or {file_name} is not a file', file=sys.stderr)
        sys.exit(1)



        # Check if the file name is composed entirely of digits
    if file_name.isdigit():
        pass
            #print('This file is named by numbers')
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




def Validate_json(content, file_name):
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
        #print(f'Content in {file_name} has been validated')
        return 1
    except ValidationError as ve:
        print(f"JSON data of {file_name} is invalid.", file=sys.stderr)
        print(ve, file=sys.stderr)


def load_check_type(type_value, height, file_path):

        unique = True

        # Check if the file exist
        if not os.path.isfile(file_path):
            print(f"File does not exist. Creating '{file_path}'...")
            try:
                # Use 'x' mode to create the file
                with open(file_path, 'x') as file:
                    print(f"File '{file_path}' created successfully.")
            except FileExistsError:
                pass

        # Read the content of 'types.txt' file
        try:
            with open(file_path, 'r') as file:
                existing_values = file.read().splitlines()
                # Check if this type is unique
                if type_value in existing_values:
                    unique = False
        except FileNotFoundError:
            # If the file does not exist, it will be checked as an empty file
            pass

        # If and only if the type is unique, it will be stored.
        if unique:
            with open(file_path, 'a') as file:  # Use 'a' mode to append the content
                file.write(type_value + '\n')
                file.write(height + '\n' + '\n')




def type_height_json(json_file, type_value, height, tx_output_path):
        json_file_path = tx_output_path + type_value + height

        # Check if the file exist
        if not os.path.isfile(json_file_path):
            print(f"File does not exist. Creating '{json_file_path}'...")
            try:
                # Use 'x' mode to create the file
                with open(json_file_path, 'x') as file:
                    print(f"File '{json_file_path}' created successfully.")
            except FileExistsError:
                pass

        with open(json_file_path, 'w') as f:
            json.dump(json_file, f, indent=4)


def decode_tx(tx, max_retries=3, retry_delay=2):
    """
    Decodes a transaction using an external API.

    Args:
        tx: The transaction to decode.
        max_retries: Maximum number of retries for the request.
        retry_delay: Time to wait between retries (in seconds).

    Returns:
        Decoded transaction if successful, None otherwise.
    """
    url = "https://lcd-terra.tfl.foundation/cosmos/tx/v1beta1/decode"
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"tx_bytes": tx})
    retries = 0

    while retries < max_retries:
        try:
            response = requests.post(url, headers=headers, data=data, timeout=5)  # Adding a 5-second timeout
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: Unable to decode transaction, server returned status code {response.status_code}", file=sys.stderr)
                if response.status_code in [502, 503, 504]:  # Retry on certain status codes
                    time.sleep(retry_delay)
                    retries += 1
                else:
                    break  # Do not retry on other errors
        except requests.exceptions.RequestException as e:
            print(f"Network request error: {e}", file=sys.stderr)
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
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

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
