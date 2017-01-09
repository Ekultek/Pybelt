import argparse
import logging
from colorlog import ColoredFormatter
from urllib2 import HTTPError
from lib.core.port_scan import PortScanner
from lib.core import BANNER
from lib.core.dork_check import DorkScanner
from lib.core.errors import GoogleBlockException
from lib.core.settings import GOOGLE_TEMP_BLOCK_ERROR_MESSAGE
from lib.core.settings import LOGGER

if __name__ == '__main__':
    opts = argparse.ArgumentParser()
    opts.add_argument('-d', '--dork-check', metavar='DORK', dest="dorkcheck",
                      help="Provide a Google dork to check for possible injectable sites")
    opts.add_argument('-c', '--hash-cracker', metavar="HASH", dest="hashcracking",
                      help="Provide a hash to crack using basic algorithms")
    opts.add_argument('-p', '--port-scanner', metavar="HOST", dest="portscan",
                      help="Provide a host to scan for open ports")
    opts.add_argument('-s', '--sqli-scanner', metavar="URL", dest="sqliscan",
                      help="Provide a URL to scan for SQL injection flaws")
    opts.add_argument('-D', '--dork-file', metavar="DORK FILE", dest="dorkfilecheck",
                      help=argparse.SUPPRESS)
    opts.add_argument('-C', '--hash-file', metavar="HASHFILE", dest="hashfilecracking",
                      help=argparse.SUPPRESS)
    args = opts.parse_args()
    print(BANNER)
    if args.dorkcheck:
        LOGGER.info("Starting dork scan, using query: '{}'..".format(args.dorkcheck))
        try:
            LOGGER.info(DorkScanner(args.dorkcheck).check_urls_for_queries())
        except HTTPError:
            LOGGER.error(GoogleBlockException(GOOGLE_TEMP_BLOCK_ERROR_MESSAGE))
            exit(1)
    if args.dorkfilecheck:
        LOGGER.info("Starting scan on file: {}".format(args.dorkfilecheck))
        with open(args.dorkfilecheck, 'r+') as data:
            for url in data.readlines():
                LOGGER.info("Running with query: {}".format(url))
                try:
                    LOGGER.info(DorkScanner(url.strip()).check_urls_for_queries())
                except HTTPError:
                    LOGGER.error(GoogleBlockException(GOOGLE_TEMP_BLOCK_ERROR_MESSAGE))
                    exit(1)
    '''if args.portscan:
        print("Starting port scanning on host: {}".format(args.portscan))
        print(PortScanner(args.portscan).connect_to_host())'''
