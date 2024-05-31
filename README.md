# Indexer Project

## Intro
Indexer Project achieves Extract, Translate, Loading (ETL) progress by using Python and Shell script, allowing users to load different information from files to database. The blocks in blockchains are the primary information to be loaded. 

## Requirement
**Python**, **PostgreSQL**, and **Shell** are required to run the project. To run the project, installation of all three softwares is required, including the Python liabraries that the Project applies. 
### Python:
#### Version: 3.10 or above 
### PostgreSQL:
#### Version: 16.2

## Installation
Before installing the dependencies, please type command:
```
pip3 install --upgrade pip
```

```
pip3 freeze
```

To install all required libraries for Python, run the following command
```
pip3 install -r requirements.txt
```

## Usage
To run the whole project, run the command git clone
```
git clone https://github.com/ziqiyang6/Indexer-Project.git
```
**Please open 'info.json' to change the path and postgreSQL login information.**

Then, run following command:
```
./tx_type.sh
```
if the command above does not work, run the following:
```
bash tx_type.sh
```
# ERD
[ERD for indexer](ERD.pdf)


