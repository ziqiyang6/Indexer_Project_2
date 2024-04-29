#!/usr/bin/python3
'''**********************************************************************************
                                                                                    *
Project Name: loading_files.py                                                         *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json          os                                                         *
                                                                                    *
Creater Name: Ziqi Yang                                                             *
                                                                                    *
Published Date: 4/15/2024                                                           *
                                                                                    *
Version: 1.0                                                                        *
                                                                                    *
Version: 1.1                                                                        *
Now the block hash is hex version                                                   *
                                                                                    *
                                                                                    *
**********************************************************************************'''

#    Scripts start below
import os
import json
from functions import check_file
from functions import create_connection
from functions import block_hash_base64_to_hex

with open('info.json', 'r') as f:
    info = json.load(f)

db_name = info['psql']['db_name']
db_user = info['psql']['db_user']
db_password = info['psql']['db_password']
db_host = info['psql']['db_host']
db_port = info['psql']['db_port']

connection = create_connection(db_name, db_user, db_password, db_host, db_port)


file_path = os.getenv('FILE_PATH')
file_name = os.getenv('FILE_NAME')

content = check_file(file_path, file_name)
block_hash = content['block_id']['hash']
block_hash_hex = block_hash_base64_to_hex(block_hash)
chain_id = content['block']['header']['chain_id']
height = content['block']['header']['height']
tx_num = len(content['block']['data']['txs'])
created_time = content['block']['header']['time']
print(block_hash, chain_id, height, tx_num, created_time)


query = """
INSERT INTO blocks (block_hash, chain_id, height, tx_num, created_at) VALUES (%s, %s, %s, %s, %s);
"""

values = (block_hash_hex, chain_id, height, tx_num, created_time)

cursor = connection.cursor()
cursor.execute(query, values)
connection.commit()
cursor.close()
