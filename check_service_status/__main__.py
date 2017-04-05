#!/usr/bin/python2

from check_service_status_module import check_service_status
import logging
import sys

logging.basicConfig( filename = 'svc_scp.log',
                     format = '%(asctime)s - %(levelname)s: %(message)s',
                     level=logging.DEBUG )

error_occured = 0
#services = ["httpd","crond"]

if len(sys.argv) < 2:
    print "Error, not enough arguments were passed."
    exit(1)
try:
    for svc in sys.argv[1:]:
        check_service_status(svc)
except:
    print("Something went wrong.")
    error_occured = 1
finally:
    print("Service check completed.")
    if error_occured == 0:
        exit(0)
    else:
        exit(1)
