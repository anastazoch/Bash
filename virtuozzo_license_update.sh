#!/bin/bash

HOSTNAME=`hostname | awk '{print toupper($0)}'`
CURRENT_DATE=`date +"%m/%d/%y"`
UPDATE_DATE=`sudo vzlicview | grep update | awk -F = '{print $2}' | awk -F '"' '{print $2}' | awk -F ' ' '{print $1}'`
EXPIRATION_DATE=`sudo vzlicview | grep expiration | awk -F '=' '{print $2}' | awk -F '"' '{print $2}' | awk -F ' ' '{print $1}'`
DAYS_REMAINING=`echo $(( ($(date --date=$EXPIRATION_DATE +%s) - $(date --date=$CURRENT_DATE +%s))/(24*60*60) ))`

if (( $(date --date=$CURRENT_DATE +%s)/(24*60*60) > $(date --date=$UPDATE_DATE +%s)/(24*60*60) ))
then
	printf "Η ενημέρωση της άδειας Virtuozzo του συστήματος %s απέτυχε.\n\nΑπομένουν %s ημέρες για λήξη της άδειας.\n\nΕπικοινωνήστε με Virtuozzo.\n" $HOSTNAME_TO_UPPERCASE $DAYS_REMAINING | mail -s "Ενημέρωση άδειας Virtuozzo" itcs@ote.gr
fi