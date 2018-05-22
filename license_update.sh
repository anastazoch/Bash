#!/bin/bash

MAIL_ADDRESS=...
HOSTNAME=`hostname | tr [a-z] [A-Z]`
UPDATE_DATE=`sudo vzlicview | grep update | awk -F = '{print $2}' | awk -F '"' '{print $2}' | awk -F ' ' '{print $1}'`
EXPIRATION_DATE=`sudo vzlicview | grep expiration | awk -F '=' '{print $2}' | awk -F '"' '{print $2}' | awk -F ' ' '{print $1}'`
DAYS_LEFT=`echo $(( ($(date --date=$EXPIRATION_DATE +%s) - $(date +%s))/(24*60*60) ))`

if (( $(date +%s)/(24*60*60) > $(date --date=$UPDATE_DATE +%s)/(24*60*60) )); then
	if (( $(date +%s)/(24*60*60) < $(date --date=$EXPIRATION_DATE +%s)/(24*60*60) )); then
		printf "System's license %s has failed.\n\n \ 
			%s days left before license expiration.\n\n \
			Please contact the ISV.\n" $HOSTNAME $DAYS_LEFT | mail -s "License update" MAIL_ADDRESS
	elif (( $(date +%s)/(24*60*60) > $(date --date=$EXPIRATION_DATE +%s)/(24*60*60) )); then
		printf "System's %s license has expired.\n\n \
		Please contact the ISV.\n" $HOSTNAME $DAYS_LEFT | mail -s "License update" MAIL_ADDRESS
	fi		
fi
