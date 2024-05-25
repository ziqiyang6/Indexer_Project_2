#!/usr/bin/env bash
#*******************************************************************************#
#                                                                               #
# FILE: tx_type.sh                                                         #
#                                                                               #
# USAGE: tx_type.sh [-h]                                                   #
#                                                                               #
# DESCRIPTION: This is a description of the script.                             #
#                                                                               #
# OPTIONS: List options for the script [-h]                                     #
#                                                                               #
# ERROR CONDITIONS: exit 1 ---- The block does not pass the validation          #
#                   exit 2 ---- The block does not pass the JSONSCHEMA test     #
#                   exit 3 ---- Cannot change to the target directory           #
#                   exit 10 --- The block does not have transaction             #
#                                                                               #
# DEVELOPER: Olaf Yang                                                      #
# DEVELOPER PHONE: +1 (516) 503-6032                                            #
# DEVELOPER EMAIL: ziqiyang91@gmail.com                                              #
#                                                                               #
# VERSION: 1.0                                                                  #
#										#
# VERSION: 1.1									#
# The path has been updated to info.json file, which means the path		#
# can be changed manually							#
# Loading files are applied in this version					#
#                                                                               #
#*******************************************************************************#
#

# Define the shell functions
#
usage(){
        echo "Usage: $0 [-h]" >&2
        exit 0
}

die()
{
        echo $1 >&2
        exit 1

}

#
# Get command line options
#
while getopts ":h" opt; do
          case $opt in
                  h) usage
                         ;;
                 \?) die "Error---->Invalid option: -$OPTARG"
                         ;;
          esac
done

# info.json path
export info_path=/Users/shikh/Library/CloudStorage/OneDrive-Personal/Documents/EMR/olaf-indexer/info.json # Change this to correct path of info.json!!

# Set the path of directory and cd to it
folder_path=$(eval echo $(jq -r '.path.block_file_path' $info_path))
cd $folder_path || { echo "Error----> Cannot change to $folder_path directory." >&2; exit 3; }

files=$(ls)


# Create log files if not exist
export txt=$(eval echo $(jq -r '.path.output_path' $info_path))
if [[ -d $txt ]]; then
    :
  else
    mkdir $txt
fi

if [[ -f $txt/output.log ]]; then
    :
  else
    touch $txt/output.log
fi

if [[ -f $txt/error.log ]]; then
    :
  else
    touch $txt/error.log
fi

# Set the path of log files
export LOG=$txt/output.log
export ERR=$txt/error.log

cd $(eval echo $(jq -r '.path.script_path' $info_path))



# Set the values of psql login info
DBNAME=$(jq -r '.psql.db_name' $info_path)
DBUSER=$(jq -r '.psql.db_user' $info_path)
DBPASSWORD=$(jq -r '.psql.db_password' $info_path)
DBHOST=$(jq -r '.psql.db_host' $info_path)
DBPORT=$(jq -r '.psql.db_port' $info_path)

# Connect to psql
PGPASSWORD=$DBPASSWORD psql -d $DBNAME -U $DBUSER -h localhost -f Txs.sql

# Select the files in the folder path and run python script 4
for file_name in $files; do
    # if folder_path does not end with /, add / to the end
    if [[ $folder_path != */ ]]; then
        folder_path="${folder_path}/"
    fi
    export FILE_PATH="${folder_path}${file_name}"
    export FILE_NAME="${file_name}"
    export txt_file_path=$(eval echo $(jq -r '.path.txt_file_path' $info_path))
    python check_one_file.py >> $LOG 2>> $ERR 
    echo "The exit code of $FILE_NAME is $? (expected 0)"
    python loading_files.py >> $LOG 2>> $ERR 
    echo "The exit code of loading $FILE_NAME is $? (expected 0)"
    python verify_block.py >> $LOG 2>> $ERR
    echo "The exit code of verifying $FILE_NAME is $? (expected 0)"

    # Define the length of transaction
    length=$(jq '.block.data.txs | length' "$FILE_PATH")
    echo "The num of transaction in $FILE_NAME is $length"

    # If number of transaction is not zero, we load the info of transaction
    if [[ $length -ne 0 ]]; then
        # For every i less than the length of transaction, make it as the ith transaction in the block
        for ((i = 0; i < $length; i++)); do
           export x=$i
           python loading_tx.py >> $LOG 2>> $ERR 
        done

    else
        :
    fi
done
exit 0
