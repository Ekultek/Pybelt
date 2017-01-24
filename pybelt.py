import argparse
import sys
import re
import random
from urllib2 import HTTPError
from lib.core import BANNER
from lib.core.errors import GoogleBlockException
from lib.core.settings import LOGGER
from lib.core.settings import LEGAL_DISC
from lib.core.settings import QUERY_REGEX
from lib.core.settings import VERSION_STRING
from lib.core.settings import create_wordlist
from lib.core.settings import WORDLIST_LINKS
from lib.core.settings import IP_ADDRESS_REGEX
from lib.core.settings import LONG_LEGAL_DISCLAIMER
from lib.core.settings import GOOGLE_TEMP_BLOCK_ERROR_MESSAGE
from lib.core.sql_scan import SQLiScanner
from lib.core.dork_check import DorkScanner
from lib.core.port_scan import PortScanner
from lib.core.hash_cracking import HashCracker

if __name__ == '__main__':
    opts = argparse.ArgumentParser()
    opts.add_argument('-d', '--dork-check', metavar='DORK', dest="dorkcheck",
                      help="Provide a Google dork to check for possible injectable sites")
    opts.add_argument('-c', '--hash-crack', metavar="HASH", dest="hash", nargs=1,
                      help="Specify a hash to crack and a hash type, IE: -c <HASH>:md5 (default all)")
    opts.add_argument('-p', '--port-scan', metavar="HOST", dest="portscan",
                      help="Provide a host to scan for open ports")
    opts.add_argument('-s', '--sqli-scanner', metavar="URL", dest="sqliscan",
                      help="Provide a URL to scan for SQL injection flaws")

    opts.add_argument('-l', '--legal', action="store_true", dest="legal",
                      help="Display the legal information")
    opts.add_argument('--version', action="store_true", dest="version",
                      help="Show the version number and exit")
    opts.add_argument('--rand-wordlist', action="store_true", dest="random_wordlist",
                      help="Use a random wordlist from a Gist link")
    args = opts.parse_args()

    print(BANNER + "\033[91m{}\033[0m".format(LEGAL_DISC) + "\n") if args.legal is False else \
        BANNER + "\033[91m{}\033[0m".format(LONG_LEGAL_DISCLAIMER + "\n")

    try:
        if args.version is True:
            LOGGER.info(VERSION_STRING)
            sys.exit(0)

        if args.random_wordlist is True:
            LOGGER.info("Creating a random wordlist..")
            create_wordlist(random.choice(WORDLIST_LINKS))
            LOGGER.info("Wordlist created, resuming process..")

        if args.sqliscan is not None:
            if QUERY_REGEX.match(args.sqliscan):
                LOGGER.info("Starting SQLi scan on {}..".format(args.sqliscan))
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

        if args.hash is not None:
            try:
                items = list(''.join(args.hash).split(":"))
                if items[1] == "all":
                    LOGGER.info("Starting hash cracking without knowledge of algorithm...")
                    HashCracker(items[0]).try_all_algorithms()
                    exit(0)
                else:
                    LOGGER.info("Starting hash cracking using %s as algorithm type" % items[1])
                    HashCracker(items[0], type=items[1]).try_certain_algorithm()
                    exit(0)
            except IndexError:
                error_message = "You must specify a hash type in order for this to word"
                exit(1)

        if args.portscan is not None and re.search(IP_ADDRESS_REGEX, sys.argv[2]):
            LOGGER.info("Starting port scan on {}".format(args.portscan))
            LOGGER.info(PortScanner(args.portscan).connect_to_host())

    except KeyboardInterrupt:
        LOGGER.error("User aborted.")
