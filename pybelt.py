import argparse
import sys
import re
import random
import socket
from urllib2 import HTTPError

# Settings information
from lib.core.errors import GoogleBlockException
from lib.core.settings import BANNER
from lib.core.settings import LOGGER
from lib.core.settings import URL_REGEX
from lib.core.settings import LEGAL_DISC
from lib.core.settings import QUERY_REGEX
from lib.core.settings import VERSION_STRING
from lib.core.settings import create_wordlist
from lib.core.settings import WORDLIST_LINKS
from lib.core.settings import IP_ADDRESS_REGEX
from lib.core.settings import LONG_LEGAL_DISCLAIMER
from lib.core.settings import GOOGLE_TEMP_BLOCK_ERROR_MESSAGE

# Class libraries that are used for the program
from lib.core.sql_scan import SQLiScanner
from lib.core.dork_check import DorkScanner
from lib.core.port_scan import PortScanner
from lib.core.hash_cracking import HashCracker
from lib.core.hash_checker import HashChecker


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
    opts.add_argument("-v", '--verify-hash', metavar="HASH", dest="hashcheck",
                      help="Verify a given hash type. (MD5, WHIRLPOOL, SHA256, etc..)")

    opts.add_argument('-l', '--legal', action="store_true", dest="legal",
                      help="Display the legal information")
    opts.add_argument('--version', action="store_true", dest="version",
                      help="Show the version number and exit")
    opts.add_argument('--rand-wordlist', action="store_true", dest="random_wordlist",
                      help="Create a random wordlist to use for dictionary attacks")
    args = opts.parse_args()

    print(BANNER + "\033[91m{}\033[0m".format(LEGAL_DISC) + "\n") if args.legal is False else \
        BANNER + "\033[91m{}\033[0m".format(LONG_LEGAL_DISCLAIMER + "\n")

    try:
        if args.version is True:  # Show the version number and exit
            LOGGER.info(VERSION_STRING)
            sys.exit(0)

        if args.random_wordlist is True: # Create a random wordlist
            LOGGER.info("Creating a random wordlist..")
            create_wordlist(random.choice(WORDLIST_LINKS))
            LOGGER.info("Wordlist created, resuming process..")

        if args.hashcheck is not None:  # Check what hash type you have
            LOGGER.info("Analyzing hash: '{}'".format(args.hashcheck))
            HashChecker(args.hashcheck).obtain_hash_type()

        if args.sqliscan is not None:  # SQLi scanning
            try:
                if QUERY_REGEX.match(args.sqliscan):
                    LOGGER.info("Starting SQLi scan on '{}'..".format(args.sqliscan))
                    LOGGER.info(SQLiScanner(args.sqliscan).sqli_search())
                else:
                    LOGGER.error("URL does not contain a query (GET) parameter. Example: http://example.com/php?id=2")
            except HTTPError as e:
                error_message = "URL: '{}' threw an exception: '{}' ".format(args.sqliscan, e)
                error_message += "and Pybelt is unable to resolve the URL, "
                error_message += "this could mean that the URL is not allowing connections "
                error_message += "or that the URL is bad. Attempt to connect "
                error_message += "to the URL manually, if a connection occurs "
                error_message += "make an issue."
                LOGGER.fatal(error_message)

        if args.dorkcheck is not None:  # Dork checker, check if your dork isn't shit
            LOGGER.info("Starting dork scan, using query: '{}'..".format(args.dorkcheck))
            try:
                LOGGER.info(DorkScanner(args.dorkcheck).check_urls_for_queries())
            except HTTPError:
                LOGGER.fatal(GoogleBlockException(GOOGLE_TEMP_BLOCK_ERROR_MESSAGE))

        if args.hash is not None:  # Try and crack a hash
            try:
                items = list(''.join(args.hash).split(":"))
                if items[1] == "all":
                    LOGGER.info("Starting hash cracking without knowledge of algorithm...")
                    HashCracker(items[0]).try_all_algorithms()
                else:
                    LOGGER.info("Starting hash cracking using %s as algorithm type.." % items[1])
                    HashCracker(items[0], type=items[1]).try_certain_algorithm()
            except IndexError:
                error_message = "You must specify a hash type in order for this to work. "
                error_message += "Example: 'python pybelt.py -c 098f6bcd4621d373cade4e832627b4f6:md5'"
                LOGGER.fatal(error_message)

        if args.portscan is not None:  # Scan a given host for open ports
            if re.search(IP_ADDRESS_REGEX, sys.argv[2]) is not None:
                LOGGER.info("Starting port scan on IP: {}".format(args.portscan))
                LOGGER.info(PortScanner(args.portscan).connect_to_host())
            elif re.search(URL_REGEX, sys.argv[2]) is not None and re.search(QUERY_REGEX, sys.argv[2]) is None:
                try:
                    LOGGER.info("Fetching resolve IP...")
                    ip_address = socket.gethostbyname(args.portscan)
                    LOGGER.info("Done! IP: {}".format(ip_address))
                    LOGGER.info("Starting scan on URL: {} IP: {}".format(args.portscan, ip_address))
                    PortScanner(ip_address).connect_to_host()
                except socket.gaierror:
                    error_message = "Unable to resolve IP address from {}.".format(args.portscan)
                    error_message += " You can manually get the IP address and try again,"
                    error_message += " dropping the query parameter in the URL (IE php?id=),"
                    error_message += " or dropping the http or https"
                    error_message += " and adding www in place of it. IE www.google.com"
                    error_message += " may fix this issue."
                    LOGGER.fatal(error_message)
            else:
                error_message = "You need to provide a host to scan,"
                error_message += " this can be given in the form of a URL "
                error_message += "or a IP address."
                LOGGER.fatal(error_message)

    except KeyboardInterrupt:  # Why you abort me?! :c
        LOGGER.error("User aborted.")
