#!/bin/bash

DIRS_TO_BACKUP=(<space-separated_directory_names>)
BACKUP_LOCAL_DIR=<local_directory_to_store_the_backup>
BACKUP_DEST_HOST=<host_to_send_the_backup>
BACKUP_DEST_DIR=<directory_in_the_remote_host_to_store_the_backup>

: '
In case the script is meant to be executed by root.
if [[ $EUID -ne 0 ]]
then
  echo "You must be the root user." 2>&1
  exit 1
fi
'

# If the array contains no directories, get directory names as arguments from the command line.
if (( ${#DIRS_TO_BACKUP[@]} < 1 ))
then
    DIRS_TO_BACKUP=("$@")
fi

# If the array contains no directories and no directory names have been passed as arguments from the command line.
if (( ( ${#DIRS_TO_BACKUP[@]} < 1 && $# < 1 ) || ( ${#DIRS_TO_BACKUP[@]} > 0 && $# > 0 ) ))
then
	echo "Error: Wrong number of directories." 2>&1
	exit 1
fi

for dir in ${DIRS_TO_BACKUP[@]}
do
    if [ -d $dir ]
    then
        tar zcpfC - `dirname $dir` `basename $dir` | ssh $BACKUP_DEST_HOST "cat > $BACKUP_DEST_DIR/`basename $dir`.tar.gz" 2> /dev/null
        if [ $? -ne 0 ]
        then
            rm -rf "$BACKUP_DIR/`basename $dir`.tar.gz"
            tar zcpfC "$BACKUP_DIR/`basename $dir`.tar.gz" `dirname $dir` `basename $dir`
        fi
    fi
done
