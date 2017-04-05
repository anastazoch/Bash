#!/usr/bin/python2

import subprocess
import logging
import os

def check_service_status(svc):
    devnull = open(os.devnull, 'w')

    logging.info('Checking if process ' + svc + ' is running.')
    service_is_running = subprocess.call(["systemctl", "status", svc], stdout=devnull)

    if service_is_running == 0:
        logging.info("%s is currently running." % svc)
    elif service_is_running == 3:
        logging.warning('Process ' + svc + ' is not running.')
        logging.info('Attempting to restart ' + svc + '.')
        service_has_restarted = subprocess.call(["systemctl", "restart", svc], stdout=devnull)

        if service_has_restarted == 0:
            logging.info("%s successfully restarted." % svc)
        elif service_has_restarted == 5:
            logging.error("Failed to restart %s.service: Unit %s.service not found." % (svc, svc))
        else:
            logging.error("Unable to restart %s. Please check the logs." % svc)
