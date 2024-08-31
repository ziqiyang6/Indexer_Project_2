#!/usr/bin/python3
"""**********************************************************************************
                                                                                    *
Project Name: load.py	                                                            *
                                                                                    *
Programming Language: Python 3                                                      *
                                                                                    *
Libraries: json          os                                                         *
                                                                                    *
Creater Name: Shikhar Gupta                                                         *
                                                                                    *
Published Date:              	                                                    *
                                                                                    *
Version: 1.0                                                                        *
************************************************************************************"""

import os
import json
import sys
import os
import json
from functions import (
    is_valid_file,
    create_connection,
    load_block,
    verify_block,
    get_num_txs,
    load_tx,
    verify_tx,
)
from psycopg2 import errors
from tqdm import tqdm


# Create postgres connection
with open("info.json", "r") as f:
    info = json.load(f)

db_name = info["psql"]["db_name"]
db_user = info["psql"]["db_user"]
db_password = info["psql"]["db_password"]
db_host = info["psql"]["db_host"]
db_port = info["psql"]["db_port"]

connection = create_connection(db_name, db_user, db_password, db_host, db_port)

# Load blocks to database
print("Loading blocks and transactions to database.")
base_path = os.getenv("BLOCK_PATH")
block_count = len(os.listdir(base_path))
tx_count = 0

for file_name in tqdm(os.listdir(base_path)):
    file_path = os.path.join(base_path, file_name)
    valid, content = is_valid_file(file_path, file_name)
    if valid:
        load_block(connection, file_path, file_name)
        verify_block(connection, file_path, file_name)
        # Load the transactions of the block
        num_txs = get_num_txs(content)
        for i in range(num_txs):
            load_tx(connection, file_path, file_name, i)
            verify_tx(connection, file_path, file_name, content, i)
            tx_count += 1

print()
print(f"{block_count} blocks were processed.")
print(f"{tx_count} transactions were processed.")
