#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: check_one_file.py                                        *
                                                                                    *
Programming Language: Python 3.11                                                    *
                                                                                    *
Libraries: json sys  os  redis 5.0.1              jsonschema 4.17.3                     *
           requests  2.31.0
                                                                        *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 2/26/2024                                                          *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
                                                                                    *
                                                                                    *
                                                                                    *
                                                                                    *
**********************************************************************************'''

####    Scripts start below
import os
import sys
from functions import check_file
from functions import height_check
from functions import Validate_json
from functions import load_check_type
from functions import type_height_json
from functions import decode_tx




tx_output_path = os.getenv('txt_file_path')
file_path = os.getenv('FILE_PATH')
file_name = os.getenv('FILE_NAME')

result = check_file(file_path, file_name)
height = height_check(result, file_name)

# Check if this file passes JSON Schema test. 1 is the specific case that passes.
if Validate_json(result, file_name) == 1:

    # Count numbers of transactions in this block
    count = len(result["block"]["data"]["txs"])

    # If there is no transaction in this block, end this progress
    if count == 0:
        sys.exit(10)

    # Use decode_tx function for each tx in this block
    for i in range(count):
        # let decoded_response be the decoded string
        decoded_response = decode_tx(result["block"]["data"]["txs"][i])
        for message in decoded_response["tx"]["body"]["messages"]:

            types = message["@type"]  # Take out the type of the transaction and store into 'types'

            load_check_type(types, height, tx_output_path)
            #type_height_json(decoded_response, types)
    print()
    sys.exit(0)
else:
   sys.exit(8)
