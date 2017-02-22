import argparse
import random
import sys

# Pointers
from lib.pointers import run_proxy_finder
from lib.pointers import run_xss_scan
from lib.pointers import run_sqli_scan
from lib.pointers import run_dork_checker
from lib.pointers import run_hash_cracker
from lib.pointers import run_hash_verification
from lib.pointers import run_port_scan

# Shell
from lib.shell import pybelt_shell

# Settings
from lib.core.settings import BANNER
from lib.core.settings import LEGAL_DISC
from lib.core.settings import LOGGER
from lib.core.settings import LONG_LEGAL_DISCLAIMER
from lib.core.settings import VERSION_STRING
from lib.core.settings import WORDLIST_LINKS
from lib.core.settings import create_wordlist


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
    opts.add_argument("-f", "--find-proxies", action="store_true", dest="proxysearch",
                      help="Attempt to find some proxies automatically")
    opts.add_argument('-x', '--xss', metavar="URL", dest="xssScan",
                      help="Check if a URL is vulnerable to XSS")

    opts.add_argument('-l', '--legal', action="store_true", dest="legal",
                      help="Display the legal information")
    opts.add_argument('--version', action="store_true", dest="version",
                      help="Show the version number and exit")
    opts.add_argument('--rand-wordlist', action="store_true", dest="random_wordlist",
                      help="Create a random wordlist to use for dictionary attacks"),
    opts.add_argument("--proxy", metavar="PROXY", dest="configProxy",
                      help="Configure the program to use a proxy when connecting")
    opts.add_argument('--rand-agent', action="store_true", dest="randomUserAgent",
                      help="Use a random user agent from a file list")
    args = opts.parse_args()

    print(BANNER + "\033[91m{}\033[0m".format(LEGAL_DISC) + "\n") if args.legal is False else \
        BANNER + "\033[91m{}\033[0m".format(LONG_LEGAL_DISCLAIMER + "\n")

    try:
        if len(sys.argv) == 1:
            prompt = pybelt_shell.PybeltConsole()
            prompt.prompt = "pybelt > "
            info_message = "You have provided no flag "
            info_message += "so you have been automatically redirected "
            info_message += "to the Pybelt Console. Type 'help run' "
            info_message += "for a list of available commands, and "
            info_message += "'run <command>' to run the command, type "
            info_message += "'quit' to exit the console.."
            try:
                prompt.cmdloop(LOGGER.info(info_message))
            except TypeError:
                LOGGER.info("Terminating session...")
                exit(0)

        if args.version is True:  # Show the version number and exit
            LOGGER.info(VERSION_STRING)
            sys.exit(0)

        if args.random_wordlist is True:  # Create a random wordlist
            LOGGER.info("Creating a random wordlist..")
            create_wordlist(random.choice(WORDLIST_LINKS))
            LOGGER.info("Wordlist created, resuming process..")

        if args.proxysearch is True:  # Find some proxies
            run_proxy_finder()

        if args.hashcheck is not None:  # Check what hash type you have
            run_hash_verification(args.hashcheck)

        if args.sqliscan is not None:  # SQLi scanning
            run_sqli_scan(args.sqliscan)

        if args.dorkcheck is not None:  # Dork checker, check if your dork isn't shit
            run_dork_checker(args.dorkcheck)

        if args.hash is not None:  # Try and crack a hash
            run_hash_cracker(args.hash)

        if args.portscan is not None:  # Scan a given host for open ports
            run_port_scan(args.portscan)

        if args.xssScan is not None:  # Scan a URL for XSS vulnerabilities
            run_xss_scan(args.xssScan, args.configProxy, args.randomUserAgent)

    except KeyboardInterrupt:  # Why you abort me?! :c
        LOGGER.error("User aborted.")
