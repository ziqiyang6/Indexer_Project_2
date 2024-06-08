#!/usr/bin/env bash
#***************************************************************************************#
#                                                                               	#
# FILE: load_transactions.sh                                                    	#
#                                                                               	#
# USAGE: load_transactions.sh -c <path> [-t] [-h] [-v]                          	#
#                                                                               	#
# DESCRIPTION: This is a description of the script.                             	#
#                                                                               	#
# OPTIONS: List options for the script [-h]                                     	#
#                                                                               	#
# ERROR CONDITIONS: exit 1 ---- Invalid option                                   	#     	                 
#                   exit 2 ---- library is not installed				#
#                   exit 3 ---- The config file does not exist				#
#                   exit 4 ---- Cannot change to the target directory    		#
#                   exit 5 ---- The block does not pass the validation test.		#
#                   exit 6 ---- The block was not successfully loaded into the database.#
#                   exit 7 ---- The block does not pass the verification test.  	#
#                   exit 8 ---- The transaction was not loaded into the database. 	#
#                   exit 9 --- Error in executing Txs.sql                    		#
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
#                                                                               	#
#***************************************************************************************#


# Define the shell functions
usage(){
        echo "
        Usage: $0 -c <path> [-t] [-h] [-v]

        Options:
                -h      Display help message.
                -c      Specify the path of the config json file. (Required)
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
info_path=""
verbose=false
block_count=0
txn_count=0
curr_dir=$(pwd)


while getopts ":c:thv" opt; do
          case $opt in
                  h) usage
                         ;;
                  c) info_path=$OPTARG
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
    die "Error---->Config file does not exist." 3
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

# Set the path of directory and cd to it
folder_path=$(eval echo $(jq -r '.path.block_file_path' $info_path))
# cd $folder_path || { die "Error---->Cannot change to the target directory" 4; }
files=$(ls $folder_path)

# Create log files if not exist
export txt=$(eval echo $(jq -r '.path.output_path' $info_path))
if [[ -d $txt ]]; then
    :
  els:e
    mkdir $txt
fi

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

# Set the path of log files
export LOG=$txt/output.log
export ERR=$txt/error.log

# Set the values of psql login info
DBNAME=$(jq -r '.psql.db_name' $info_path)
DBUSER=$(jq -r '.psql.db_user' $info_path)
DBPASSWORD=$(jq -r '.psql.db_password' $info_path)
DBHOST=$(jq -r '.psql.db_host' $info_path)
DBPORT=$(jq -r '.psql.db_port' $info_path)

export txt_file_path=$(eval echo $(jq -r '.path.txt_file_path' $info_path))

cd $(eval echo $(jq -r '.path.script_path' $info_path))

# Connect to psql
PGPASSWORD=$DBPASSWORD psql -d $DBNAME -U $DBUSER -h localhost -f Txs.sql --quiet --set ON_ERROR_STOP=1

if [[ $? -ne 0 ]]; then
    die "Error---->Txs.sql had an error. (Exit code $?). Check log file for more information" 9
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

for file_name in $files; do
    # if folder_path does not end with /, add / to the end
    if [[ $folder_path != */ ]]; then
        folder_path="${folder_path}/"
    fi
    export FILE_PATH="${folder_path}${file_name}"
    export FILE_NAME="${file_name}"
    # if python_three is true, run python3
    if [[ $python_three == true ]]; then
        python3 check_one_file.py >> $LOG 2>> $ERR
        # Error code 8 means the block does not pass the validation
        if [[ $? == 8 ]]; then
            die "$FILE_NAME does not pass the JSON validation. (Exit code $?). Check log file for more information" 5
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME passes the JSON validation."
        fi
        python3 loading_files.py >> $LOG 2>> $ERR
        if [[ $? -ne 0 ]]; then
            die "$FILE_NAME loading into database failed. (Exit code $?). Check log file for more information" 6
            continue
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME is successfully loaded into the database."
        fi
        python3 verify_block.py >> $LOG 2>> $ERR
        if [[ $? -ne 0 ]]; then
            die "$FILE_NAME does not pass the verification test. (Exit code $?). Check log file for more information" 7
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME passes the verification test."
        fi
        block_count=$((block_count+1))
    else
        python check_one_file.py >> $LOG 2>> $ERR
        if [[ $? == 8 ]]; then
            die "$FILE_NAME does not pass the JSON validation. (Exit code $?). Check log file for more information" 5
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME passes the JSON validation."
        fi
        python loading_files.py >> $LOG 2>> $ERR
        if [[ $? -ne 0 ]]; then
            die "$FILE_NAME loading into database failed. (Exit code $?). Check log file for more information" 6
            continue
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME is successfully loaded into the database."
        fi
        python verify_block.py >> $LOG 2>> $ERR
        if [[ $? -ne 0 ]]; then
            die "$FILE_NAME does not pass the verification test. (Exit code $?). Check log file for more information" 7
        elif [[ $verbose == true ]]; then
            echo -e "$FILE_NAME passes the verification test."
        fi
        block_count=$((block_count+1))
    fi


    # Define the length of transaction
    length=$(jq '.block.data.txs | length' "$FILE_PATH")
    if [[ $verbose == true ]]; then
        echo "$length transactions were found."
    fi

    # If number of transaction is not zero, we load the info of transaction
    if [[ $length -ne 0 ]]; then
        # For every i less than the length of transaction, make it as the ith transaction in the block
        for ((i = 0; i < $length; i++)); do
            export x=$i
            if [[ $python_three == true ]]; then
                python3 loading_tx.py >> $LOG 2>> $ERR
                if [[ $? -ne 0 ]]; then
                    die "Error---->Transaction $i in $FILE_NAME loading into database failed. (Exit code $?). Check log file for more information" 8
                fi
            else
                python loading_tx.py >> $LOG 2>> $ERR 
                if [[ $? -ne 0 ]]; then
                    die "Error---->Transaction $i in $FILE_NAME loading into database failed. (Exit code $?). Check log file for more information" 8
                fi
            fi
            txn_count=$((txn_count+1))
        done
        if [[ $verbose == true ]]; then
            echo "$length transactions in $FILE_NAME loaded into the database."
        fi
    else
        echo "There are no transactions in $FILE_NAME."
    fi
done
echo ""
echo "$block_count blocks were processed."
echo "$txn_count transactions were processed."
exit 0
