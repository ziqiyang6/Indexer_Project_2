# Indexer Project

## Intro
Indexer Project achieves Extract, Translate, Loading (ETL) progress by using Python and Shell script, allowing users to load different information from files to database. The blocks in blockchains are the primary information to be loaded. 

## Requirement
**Python3**, **PostgreSQL**, **JQ**, and **Shell** are required to run the project. To run the project, installation of all three softwares is required, including the Python liabraries that the Project applies. 
### Python:
#### Version: 3.10 or above 
### PostgreSQL:
#### Version: 16.2
### JQ:
#### Version: 1.7.1

## Installation
*Note: If using python3 command, replace all instances of pip with pip3.*

Before installing the dependencies, please type command:
```
pip install --upgrade pip
```

```
pip freeze
```

To install all required libraries for Python, run the following command
```
pip install -r requirements.txt
```

## Usage
To run the whole project, run the command git clone
```
git clone https://github.com/ziqiyang6/Indexer_Project_2
```
**Please open 'info.json.template', copy this file to a new file called 'info.json', and input the postgreSQL login information. Do not input any personal information into info.json.template.**

*For the `db_name` field, ensure this database already exists.*

**This script requires a folder containing decrypted blocks to be parsed.**

Then, from the root directory of the repository, run following command:
```
./load_transactions.sh -b <block folder location>
```
or if using the `python3` command, run:
```
./load_transactions.sh -b <block folder location> -t
```
if the command above does not work, run the following:
```
bash load_transactions.sh -b <block folder location>
```
or 
```
bash load_transactions.sh -b <block folder location> -t
```
# ERD
[ERD for indexer](ERD.pdf)


