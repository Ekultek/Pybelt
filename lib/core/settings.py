import random
import os
import uuid
import re

# Full path to everything
PATH = os.getcwd()

# Current version
VERSION = "1.0"

# Clone link
CLONE_LINK = "https://github.com/ekultek/pybelt.git"

# Basic legal disclaimer
LEGAL_DISC = "legal disclaimer: This program is intended for learning purposes, any malicious intent is on you, it is the end users responsibility to obey all laws, regulations, and rules of your respective country or place of origin. For further information about this please see the legal information file under docs or run the --legal flag"

# Version string, dev or stable
VERSION_STRING = "%s(dev)" % VERSION if len(VERSION) >= 4 else "%s(stable)" % VERSION

# Random dork to use for basic sqli searches
RANDOM_DORK = random.choice(open("{}/lib/core/text_files/dorks.txt".format(PATH)).readlines())

# Random saying to display on the banner
RANDOM_SAYING = random.choice(open("{}/lib/core/text_files/sayings.txt".format(PATH)).readlines())

# Random common column names
RANDOM_COMMON_COLUMN = random.choice(open("{}/lib/core/text_files/common_columns.txt".format(PATH)).readlines())

# Search query regex to make sure the URLS have a GET parameter
QUERY_REGEX = re.compile(r"(.*)[?|#](.*){1}\=(.*)")

# Sexy ass banner
BANNER = """
 ____  __ __  ____     ___  _     ______
|    \|  |  ||    \   /  _]| |   |      |
|  o  )  |  ||  o  ) /  [_ | |   |      |
|   _/|  ~  ||     ||    _]| |___|_|  |_|
|  |  |___, ||  O  ||   [_ |     | |  |
|  |  |     ||     ||     ||     | |  |
|__|  |____/ |_____||_____||_____| |__|  %s

%s
%s

[!] %s\n\n
""" % (VERSION_STRING, RANDOM_SAYING.strip(), CLONE_LINK, LEGAL_DISC)

# Path the the search results from a dork scan
DORK_SCAN_RESULTS_PATH = r"{}\lib\core\dork_check\scan_results".format(os.getcwd())

# Error message for when Google blocks your IP address
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE = "\nYou have been temporarily blocked from running Google searches."
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += " As of now there is no way around this. You will need to:\n"
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += "\tA) Change your IP address.\n"
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += "\tB) Wait about an hour for Google to lift the ban.\n"
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += "\tC) Manually check your Dorks."

# List of reserved port numbers, these are the ports that you want to check
RESERVED_PORTS = {
    1, 5, 7, 18, 20, 21, 22, 23, 25, 29, 37,  42, 43, 49, 53, 69, 70,
    79, 80, 103, 108, 109, 110, 115, 118, 119, 137, 139, 143, 150, 156,
    161, 179, 190, 194, 197, 389, 396, 443, 444, 445, 458, 546, 547, 563,
    569, 1080
}

# All of the ports and what they are used for
PORT_DESCRIPTIONS = {
    '1': "TCP Port Service Multiplexer (TCPMUX)", '5': "Remote Job Entry (RJE)", '7': "ECHO",
    '18': "Message Send Protocol (MSP)",
    '20': "FTP -- Data", '21': "FTP -- Control", '22': "SSH Remote Login Protocol", '23': "Telnet",
    '25': "Simple Mail Transfer Protocol (SMTP)", '29': "MSG ICP", '37': "Time", '42': "Host Name Server (Nameserv)",
    '43': "WhoIs", '49': "Login Host Protocol (Login)", '53': "Domain Name System (DNS)",
    '69': "Trivial File Transfer Protocol (TFTP)",
    '70': "Gopher Services", '79': "Finger", '80': "HTTP", '103': "X.400 Standard",
    '108': "SNA Gateway Access Server", '109': "POP2", '110': "POP3", '115': "Simple File Transfer Protocol (SFTP)",
    '118': "SQL Services", '119': "Newsgroup (NNTP)", '137': "NetBIOS Name Service", '139': "NetBIOS Datagram Service",
    '143': "Interim Mail Access Protocol (IMAP)", '150': "NetBIOS Session Service", '156': "SQL Server", '161': "SNMP",
    '179': "Border Gateway Protocol (BGP)", '190': "Gateway Access Control Protocol (GACP)",
    '194': "Internet Relay Chat (IRC)", '197': "Directory Location Service (DLS)",
    '389': "Lightweight Directory Access Protocol (LDAP)", '396': "Novell Netware over IP", '443': "HTTPS",
    '444': "Simple Network Paging Protocol (SNPP)",
    '445': "Microsoft-DS", '458': "Apple QuickTime", '546': "DHCP Client", '547': "DHCP Server",
    '563': "SNEWS", '569': "MSN", '1080': "Socks"
}


def create_random_filename():
    """ Create a random file name
    >>> print(create_random_filename())
    56558c08-ee1f-40b4-b048-be4c4066f8b6 """
    return str(uuid.uuid4())
