#!/usr/bin/env bash
#***************************************************************************************#
#                                                                               	#
# FILE: load_transactions.sh                                                    	#
#                                                                               	#
# USAGE: load_transactions.sh -b <path> -o <path> [-t] [-h] [-v]                        #
#                                                                               	#
# DESCRIPTION: This is a description of the script.                             	#
#                                                                               	#
# OPTIONS: List options for the script [-h]                                     	#
#                                                                               	#
# ERROR CONDITIONS: exit 1 ---- Invalid option                                   	#     	                 
#                   exit 2 ---- library is not installed				#
#                   exit 3 ---- File/directory passed in does not exist or        	#
#                               could not be created.				        #
#                   exit 4 ---- Cannot change to the target directory    		#
#                   exit 5 --- Error in executing Txs.sql                    		#
#                   exit 6 --- Error in loading the blocks into the database		#
#                                                                               	#
# DEVELOPER: Olaf Yang and Shikhar Gupta                                      		#
# DEVELOPER PHONE: +1 (516) 503-6032                                            	#
# DEVELOPER EMAIL: ziqiyang91@gmail.com, shikhar.gupta.tx@gmail.com                    	#
#                                                                               	#
# VERSION: 1.0                                                                  	#
#											#
# VERSION: 1.1										#
# The path has been updated to info.json file, which means the path			#
# can be changed manually								#
# Loading files are applied in this version						#
#											#
# VERSION: 1.2										#
# Filename update and arguments added.							#
# Verification of blocks check added.							#
#                                                                            		#
# VERSION: 1.3										#
# Removed dependency on explicit filepaths within info.json.                    	#
#                                                                               	#
#***************************************************************************************#


# Define the shell functions
usage(){
        echo "
        Usage: $0 -b <path> [-o <path>] [-t] [-h] [-v]

        Options:
                -h      Display help message.
                -b      Specify the folder where the blocks are stored. (Required)
                -o      Specify the folder where the output log files are to be stored. (Default is $(pwd)/log)
                -t      Use python3 alias to run the script. (Default is python)
                -v      Verbose mode. (Default is off)
        " >&2

        exit 0
}

die()
{
    echo -e "$1" >&2
    exit $2
}


#
# Get command line options
#
python_three=false
info_path=$(pwd)/info.json
folder_path=""
txt=$(pwd)/log
verbose=false
block_count=0
txn_count=0


while getopts ":i:b:o:thv" opt; do
          case $opt in
                  h) usage
                         ;;
                  b) folder_path=$OPTARG
                         ;;
                  o) txt=$OPTARG
                         ;;
                  t) python_three=true
                         ;;
                  v)  verbose=true
                         ;;
                  \?) die "Error---->Invalid option: -$OPTARG" 1
                         ;;
          esac
done

# Check if the config file exists
if [[ ! -f $info_path ]]; then
    die "Error---->info.json file does not exist." 3
fi

# Check if the block path exists and is a directory
if [[ ! -d $folder_path ]]; then
    die "Error---->Block path does not exist or is not a directory." 3
fi

# Check if the output path exists
if [[ ! -d $txt ]]; then
    # Create the output path if it does not exist
    mkdir -p $txt
    # Check if the output path was created successfully
    if [[ $? -ne 0 ]]; then
        die "Error---->Output path does not exist and could not be created." 3
    fi
fi

# Ensure python is installed
if [[ $python_three == true ]]; then
    if ! command -v python3 &> /dev/null; then
        die "Error---->python3 is not installed." 2
    fi
else
    if ! command -v python &> /dev/null; then
        die "Error---->python is not installed." 2
    fi
fi

# Ensure psql is installed
if ! command -v psql &> /dev/null; then
    die "Error---->postgresql not installed." 2
fi

# Ensure jq is installed
if ! command -v jq &> /dev/null; then
    die "Error---->jq is not installed." 2
fi

# info.json path
export info_path=$info_path

# Get block files from the folder
# folder_path=$(eval echo $(jq -r '.path.block_file_path' $info_path))
# cd $folder_path || { die "Error---->Cannot change to the target directory" 4; }
files=$(ls $folder_path)

# Create log files if not exist
# export txt=$(eval echo $(jq -r '.path.output_path' $info_path))
# if [[ -d $txt ]]; then
#     :
#   else
#     mkdir $txt
# fi

if [[ -f $txt/output.log ]]; then
    rm $txt/output.log #:
  else
    touch $txt/output.log
fi

if [[ -f $txt/error.log ]]; then
    rm $txt/error.log
  else
    touch $txt/error.log
fi

if [[ -f $txt/output2.log ]]; then
    rm $txt/output2.log #:
  else
    touch $txt/output2.log
fi

if [[ -f $txt/test.log ]]; then
    rm $txt/test.log #:
  else
    touch $txt/test.log
fi

# Set the path of log files
export LOG=$txt/output.log
export OUT=$txt/output2.log
export TEST=$txt/test.log
export ERR=$txt/error.log

# Set the values of psql login info
DBNAME=$(jq -r '.psql.db_name' $info_path)
DBUSER=$(jq -r '.psql.db_user' $info_path)
DBPASSWORD=$(jq -r '.psql.db_password' $info_path)
DBHOST=$(jq -r '.psql.db_host' $info_path)
DBPORT=$(jq -r '.psql.db_port' $info_path)

# echo "Database Name: $DBNAME"
# echo "Database User: $DBUSER"
# echo "Database Password: $DBPASSWORD"
# echo "Database Host: $DBHOST"
# echo "Database Port: $DBPORT"

# export txt_file_path=$(eval echo $(jq -r '.path.txt_file_path' $info_path))

# cd $(eval echo $(jq -r '.path.script_path' $info_path))

# Connect to psql

PGPASSWORD=$DBPASSWORD psql -d $DBNAME -U $DBUSER -h localhost -f Txs.sql --quiet --set ON_ERROR_STOP=1

if [[ $? -ne 0 ]]; then
    die "Error---->Txs.sql had an error. (Exit code $?). Check log file for more information" 5
fi
if [[ $verbose == true ]]; then
    echo "Txs.sql has been executed."
fi

# Select the files in the folder path and run python script 4
num_blocks=$(ls $folder_path | wc -l)
bar_size=40
bar_char_done="#"
bar_char_todo="-"
bar_percentage_scale=2

export BLOCK_PATH="${folder_path}"

if [[ $python_three == true ]]; then
    # get the return value of the python script
    python3 load.py
else
    python load.py
fi

if [[ $? -ne 0 ]]; then
    die "Error---->The blocks and transactions were not successfully loaded into the database." 6
fi
exit 0
