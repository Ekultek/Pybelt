import re
import socket
from urllib2 import HTTPError

# Libraries
from lib.core.dork_check import DorkScanner
from lib.core.errors import GoogleBlockException
from lib.core.hash_cracking import HashCracker
from lib.core.hash_cracking.hash_checker import HashChecker
from lib.core.port_scan import PortScanner
from lib.core.proxy_finder import attempt_to_connect_to_proxies
from lib.core.sql_scan.xss_scan import xss
from lib.core.sql_scan import SQLiScanner

# Settings
from lib.core.settings import GOOGLE_TEMP_BLOCK_ERROR_MESSAGE
from lib.core.settings import IP_ADDRESS_REGEX
from lib.core.settings import LOGGER
from lib.core.settings import QUERY_REGEX
from lib.core.settings import URL_REGEX
from lib.core.settings import RANDOM_USER_AGENT
from lib.core.settings import prompt


def run_sqli_scan(url, url_file=None, proxy=None, user_agent=False, tamper=None):
    """ Pointer to run a SQLi Scan on a given URL """
    error_message = "URL: '{}' threw an exception ".format(url)
    error_message += "and Pybelt is unable to resolve the URL, "
    error_message += "this could mean that the URL is not allowing connections "
    error_message += "or that the URL is bad. Attempt to connect "
    error_message += "to the URL manually, if a connection occurs "
    error_message += "make an issue."

    if url_file is not None:  # Run through a file list
        file_path = url_file
        total = len(open(file_path).readlines())
        done = 0
        LOGGER.info("Found a total of {} urls in file {}..".format(total, file_path))
        with open(file_path) as urls:
            for url in urls.readlines():
                try:
                    if QUERY_REGEX.match(url.strip()):
                        question = prompt("Would you like to scan '{}' for SQLi vulnerabilities[y/N]: ".format(
                            url.strip()
                        ))
                        if question.lower().startswith("y"):
                            LOGGER.info("Starting scan on url: '{}'".format(url.strip()))
                            LOGGER.info(SQLiScanner(url.strip()).sqli_search())
                            done += 1
                            LOGGER.info("URLS scanned: {}, URLS left: {}".format(done, total - done))
                        else:
                            pass
                    else:
                        LOGGER.warn("URL '{}' does not contain a query (GET) parameter, skipping..".format(url.strip()))
                        pass
                except HTTPError:
                    LOGGER.fatal(error_message)
        LOGGER.info("No more URLS found in file, shutting down..")

    else:  # Run a single URL
        try:
            if QUERY_REGEX.match(url):
                LOGGER.info("Starting SQLi scan on '{}'..".format(url))
                LOGGER.info(SQLiScanner(url).sqli_search())
            else:
                LOGGER.error("URL does not contain a query (GET) parameter. Example: http://example.com/php?id=2")
        except HTTPError:
            LOGGER.fatal(error_message)


def run_xss_scan(url, url_file=None, proxy=None, user_agent=False):
    """ Pointer to run a XSS Scan on a given URL """
    proxy = proxy if proxy is not None else None
    header = RANDOM_USER_AGENT if user_agent is not False else None
    if proxy is not None:
        LOGGER.info("Proxy configured, running through: {}".format(proxy))
    if user_agent is True:
        LOGGER.info("Grabbed random user agent: {}".format(header))

    if url_file is not None:  # Scan a given file full of URLS
        file_path = url_file
        total = len(open(url_file).readlines())
        done = 0
        LOGGER.info("Found a total of {} URLS to scan..".format(total))
        with open(file_path) as urls:
            for url in urls.readlines():
                if QUERY_REGEX.match(url.strip()):
                    question = prompt("Would you like to scan '{}' for XSS vulnerabilities[y/N]: ".format(url.strip()))
                    if question.lower().startswith("y"):
                        done += 1
                        if not xss.main(url.strip(), proxy=proxy, headers=header):
                            LOGGER.info("URL '{}' does not appear to be vulnerable to XSS".format(url.strip()))
                        else:
                            LOGGER.info("URL '{}' appears to be vulnerable to XSS".format(url.strip()))
                        LOGGER.info("URLS scanned: {}, URLS left: {}".format(done, total - done))
                    else:
                        pass
                else:
                    LOGGER.warn("URL '{}' does not contain a query (GET) parameter, skipping".format(url.strip()))
        LOGGER.info("All URLS in file have been scanned, shutting down..")

    else:  # Scan a single URL
        if QUERY_REGEX.match(url):
            LOGGER.info("Searching: {} for XSS vulnerabilities..".format(url, proxy=proxy, headers=header))
            if not xss.main(url, proxy=proxy, headers=header):
                LOGGER.error("{} does not appear to be vulnerable to XSS".format(url))
            else:
                LOGGER.info("{} seems to be vulnerable to XSS.".format(url))
        else:
            error_message = "The URL you provided does not contain a query "
            error_message += "(GET) parameter. In order for this scan you run "
            error_message += "successfully you will need to provide a URL with "
            error_message += "A query (GET) parameter example: http://127.0.0.1/php?id=2"
            LOGGER.fatal(error_message)


def run_port_scan(host):
    """ Pointer to run a Port Scan on a given host """
    if re.search(IP_ADDRESS_REGEX, host) is not None:
        LOGGER.info("Starting port scan on IP: {}".format(host))
        LOGGER.info(PortScanner(host).connect_to_host())
    elif re.search(URL_REGEX, host) is not None and re.search(QUERY_REGEX, host) is None:
        try:
            LOGGER.info("Fetching resolve IP...")
            ip_address = socket.gethostbyname(host)
            LOGGER.info("Done! IP: {}".format(ip_address))
            LOGGER.info("Starting scan on URL: {} IP: {}".format(host, ip_address))
            PortScanner(ip_address).connect_to_host()
        except socket.gaierror:
            error_message = "Unable to resolve IP address from {}.".format(host)
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


def run_hash_cracker(hash_to_crack, hash_file=None):
    """ Pointer to run the Hash Cracking system """
    try:
        items = list(''.join(hash_to_crack).split(":"))
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


def run_hash_verification(hash_to_verify, hash_ver_file=None):
    """ Pointer to run the Hash Verification system"""
    LOGGER.info("Analyzing hash: '{}'".format(hash_to_verify))
    HashChecker(hash_to_verify).obtain_hash_type()


def run_dork_checker(dork, dork_file=None):
    """ Pointer to run a Dork Check on a given Google Dork """
    LOGGER.info("Starting dork scan, using query: '{}'..".format(dork))
    try:
        LOGGER.info(DorkScanner(dork).check_urls_for_queries())
    except HTTPError:
        LOGGER.fatal(GoogleBlockException(GOOGLE_TEMP_BLOCK_ERROR_MESSAGE))


def run_proxy_finder():
    """ Pointer to run Proxy Finder """
    LOGGER.info("Starting proxy search..")
    attempt_to_connect_to_proxies()