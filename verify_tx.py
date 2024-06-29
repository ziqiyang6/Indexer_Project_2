'''**********************************************************************************
                                                                                    *
Project Name:  verify_tx.py                                                         *
                                                                                    *
Programming Language: Python 3.11                                                   *
                                                                                    *
Libraries: json, psycopg2, os, datetime                                             *
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
import os
import sys
import json
from functions import check_file
from functions import create_connection
from functions import block_hash_base64_to_hex
from functions import hash_to_hex, decode_tx, ordered, replace_dict, time_parse
from psycopg2 import errors#  compare_nested_json,
from datetime import datetime, timedelta, timezone

with open("info.json", "r") as f:
    info = json.load(f)

db_name = info["psql"]["db_name"]
db_user = info["psql"]["db_user"]
db_password = info["psql"]["db_password"]
db_host = info["psql"]["db_host"]
db_port = info["psql"]["db_port"]

connection = create_connection(db_name, db_user, db_password, db_host, db_port)

#block_path = info["path"]["block_file_path"]
#for dirName, subDirList, fileList in os.walk(block_path):
    #for file in fileList:
        
file_path = os.getenv("FILE_PATH")
file_name = os.getenv("FILE_NAME")
output_path = os.getenv('txt')
content = check_file(file_path, file_name)
num = os.getenv('x')

block_hash = content["block_id"]["hash"]
block_hash_hex = block_hash_base64_to_hex(block_hash)
chain_id = content["block"]["header"]["chain_id"]
height = content["block"]["header"]["height"]
tx_num = str(len(content["block"]["data"]["txs"]))
created_time = content["block"]["header"]["time"]

transaction_string = content['block']['data']['txs'][int(num)]
decoded_response = decode_tx(transaction_string)
#print(decoded_response)
tx_hash = hash_to_hex(transaction_string)
order = int(num) + 1
loadedCorrectly = True
cursor = connection.cursor()
search_query = f"SELECT block_id FROM blocks WHERE height = '{height}'" # Search the block hash from the block
cursor.execute(search_query)
result = cursor.fetchall()
##########block_id =
trans_values ={
    'block_id': result[0][0],
    'tx_hash': hash_to_hex(transaction_string),
    'chain_id':  content["block"]["header"]["chain_id"],
    'height':  content["block"]["header"]["height"],
    'memo':  decoded_response['tx']['body']['memo'],
    'fee_denom': decoded_response['tx']['auth_info']['fee']['amount'][0]['denom'],
    'fee_amount': decoded_response['tx']['auth_info']['fee']['amount'][0]['amount'],
    'gas_limit': decoded_response['tx']['auth_info']['fee']['gas_limit'],
    'created_at': content['block']['header']['time'],
    'tx_info': json.dumps(decoded_response),
    'comment': f'This is number {order} transaction in BLOCK {height}'
}
print(decoded_response)
try:
    query = f"SELECT block_id, tx_hash, chain_id, height, memo, fee_denom, fee_amount, gas_limit, created_at, tx_info, comment FROM transactions WHERE height = %s"
    cursor.execute(query, (height,))
    row = cursor.fetchall()
    
    if row is None or len(row) != 1:
        loadedCorrectly = False
        #print("error")
    else:
        row = row[0]
        colnames =  [desc[0] for desc in cursor.description]
        row_dict = dict(zip(colnames, row))
        for col in trans_values:
            #print(trans_values[col])
            #print(row_dict[col])_tx
            db_info = str(row_dict[col])
            block_info = trans_values[col]
            
            if col == 'created_at':
                #print(block_info)
                #print(db_info)
                
                formatted_dt = time_parse(trans_values[col])
                block_info = formatted_dt
                
            if col == 'tx_info':
                try:
                    db_tx_info = json.dumps(row_dict[col])
                    db_info = json.loads(db_tx_info)
                    block_info = json.loads(trans_values[col])
                except json.JSONDecodeError as e:
                    print("JSONDecodeError:", e)
                    print(f"Error in block " + file_name)

            if block_info != db_info:
                ###
                #print(block_info)
                print("error")
                #print(db_info)
               
             
except errors.UniqueViolation as e:
    pass