#!/bin/bash

USERS=(<space-separated_user_names>)
GROUPS=(<space-separated_group_name>)
DEFAULT_PASSWORD=<default_password>

for user in ${USERS[@]}
do
	useradd $user
	echo $DEFAULT_PASSWORD | passwd $user --stdin
	chage -d 0 $user
	
	for group in ${GROUPS[@]}
	do
		usermod -a -G $group $user
	done	
done