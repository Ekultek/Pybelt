import argparse
import sys
import re
from urllib2 import HTTPError
from lib.core import BANNER
from lib.core.errors import GoogleBlockException
from lib.core.settings import LOGGER
from lib.core.settings import LEGAL_DISC
from lib.core.settings import QUERY_REGEX
from lib.core.settings import VERSION_STRING
from lib.core.settings import IP_ADDRESS_REGEX
from lib.core.settings import LONG_LEGAL_DISCLAIMER
from lib.core.settings import GOOGLE_TEMP_BLOCK_ERROR_MESSAGE
from lib.core.sql_scan import SQLiScanner
from lib.core.dork_check import DorkScanner
from lib.core.port_scan import PortScanner

if __name__ == '__main__':
    opts = argparse.ArgumentParser()
    opts.add_argument('-d', '--dork-check', metavar='DORK', dest="dorkcheck",
                      help="Provide a Google dork to check for possible injectable sites")
    opts.add_argument('-c', '--hash-cracker', metavar="HASH", dest="hashcracking",
                      help=argparse.SUPPRESS)
    opts.add_argument('-p', '--port-scanner', metavar="HOST", dest="portscan",
                      help="Provide a host to scan for open ports")
    opts.add_argument('-s', '--sqli-scanner', metavar="URL", dest="sqliscan",
                      help="Provide a URL to scan for SQL injection flaws")
    opts.add_argument('-D', '--dork-file', metavar="DORK FILE", dest="dorkfilecheck",
                      help=argparse.SUPPRESS)
    opts.add_argument('-C', '--hash-file', metavar="HASHFILE", dest="hashfilecracking",
                      help=argparse.SUPPRESS)
    opts.add_argument('-l', '--legal', action="store_true", dest="legal",
                      help="Display the legal information")
    opts.add_argument('--version', action="store_true", dest="version",
                      help="Show the version number and exit")
    args = opts.parse_args()

    print(BANNER + "\033[91m{}\033[0m".format(LEGAL_DISC) + "\n") if args.legal is False else \
        BANNER + "\033[91m{}\033[0m".format(LONG_LEGAL_DISCLAIMER + "\n")

    try:
        if args.version is True:
            LOGGER.info(VERSION_STRING)
            sys.exit(0)

        if args.sqliscan is not None:
            if QUERY_REGEX.match(args.sqliscan):
                LOGGER.info("Starting SQLi scan on {}".format(args.sqliscan))
                LOGGER.info(SQLiScanner(args.sqliscan).sqli_search())
            else:
                LOGGER.error("URL does not contain a query (GET) parameter. Example: http://example.com/php?id=2")

        if args.dorkcheck is not None:
            LOGGER.info("Starting dork scan, using query: '{}'..".format(args.dorkcheck))
            try:
                LOGGER.info(DorkScanner(args.dorkcheck).check_urls_for_queries())
            except HTTPError:
                LOGGER.fatal(GoogleBlockException(GOOGLE_TEMP_BLOCK_ERROR_MESSAGE))
                exit(1)

        if args.portscan and re.search(IP_ADDRESS_REGEX, sys.argv[2]) is not None:
            LOGGER.info("Starting port scan on {}".format(args.portscan))
            LOGGER.info(PortScanner(args.portscan).connect_to_host())
        else:
            LOGGER.fatal("You must provide a host (IP) to scan, example: 127.0.0.1")

    except KeyboardInterrupt:
        LOGGER.error("User aborted.")

    print("Running with {}".format(sys.argv))
