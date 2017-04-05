#!/bin/bash

HOSTNAME=`hostname | awk '{print toupper($0)}'`
UPDATE_DATE=`sudo vzlicview | grep update | awk -F = '{print $2}' | awk -F '"' '{print $2}' | awk -F ' ' '{print $1}'`
EXPIRATION_DATE=`sudo vzlicview | grep expiration | awk -F '=' '{print $2}' | awk -F '"' '{print $2}' | awk -F ' ' '{print $1}'`
DAYS_LEFT=`echo $(( ($(date --date=$EXPIRATION_DATE +%s) - $(date +%s))/(24*60*60) ))`

if (( $(date +%s)/(24*60*60) > $(date --date=$UPDATE_DATE +%s)/(24*60*60) )); then
	printf "License update in the system %s has failed.\n\n \ 
	%s days left before your license expires.\n\n \
	Please contact Virtuozzo.\n" $HOSTNAME_TO_UPPERCASE $DAYS_LEFT | mail -s "Ενημέρωση άδειας Virtuozzo" itcs@ote.gr
fi
