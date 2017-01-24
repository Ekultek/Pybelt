import os
import uuid
import re
import logging
import random
import time
import urllib2
import base64
from colorlog import ColoredFormatter

log_level = logging.INFO
logger_format = "[%(log_color)s%(asctime)s %(levelname)s%(reset)s] %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(log_level)
formatter = ColoredFormatter(logger_format, datefmt="%I:%M:%S")
stream = logging.StreamHandler()
stream.setLevel(log_level)
stream.setFormatter(formatter)
LOGGER = logging.getLogger('pybeltConfig')
LOGGER.setLevel(log_level)
LOGGER.addHandler(stream)

# Full path to everything
PATH = os.getcwd()

# Current version
VERSION = "1.1.2"

# Coloring for the version string
TYPE_COLORS = {"dev": 33, "stable": 92}

# Type of version that the program is in "dev" or "stable"
VERSION_STRING = "\033[92m{}\033[0m(\033[{}m\033[1mdev\033[0m)".format(VERSION, TYPE_COLORS["dev"]) if len(
    VERSION) >= 4 else \
    "\033[92m{}\033[0m(\033[{}m\033[1mstable\033[0m)".format(VERSION, TYPE_COLORS["stable"])

# Clone link
CLONE_LINK = "https://github.com/ekultek/pybelt.git"

# Basic legal disclaimer
LEGAL_DISC = "[!] legal disclaimer: This program is intended for learning purposes, any malicious intent is on you, " \
             "it is the end users responsibility to obey all laws, regulations, and rules of your respective country " \
             "or place of origin. For further information about this please see the legal information file under docs " \
             "or run the --legal flag"
LONG_LEGAL_DISCLAIMER = open("lib/text_files/legal.txt").read()

# Random saying to display on the banner
SAYING = random.choice(["The Hackers ToolBelt..",
                        "The Hackers Blackbelt..",
                        "The Hackers Multi-Tool..",
                        "The Hackers Gerber.."])

# Random common column names
RANDOM_COMMON_COLUMN = random.choice(open("{}/lib/text_files/common_columns.txt".format(PATH)).readlines())

# Search query regex to make sure the URLS have a GET parameter
QUERY_REGEX = re.compile(r"(.*)[?|#](.*){1}\=(.*)")

SQLI_ERROR_REGEX = (
    re.compile(r"SQL syntax.*MySQL"),  # You have an error in your SQL syntax
    re.compile("Warning.*mysql_.*"),  # Warning MySQL syntax contains an error at line ..
    re.compile(r"valid MySQL result"),  # Your search has produced a invalid MySQL result
    re.compile(r"MySqlClient\."),  # You have an error located at .. in your MySQL client server
)

SYNTAX_REGEX = re.compile(r"\W+$")

IP_ADDRESS_REGEX = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

# Sexy ass banner
BANNER = """\033[94m
  |                          /_/    |
- * -                       /_/   - * -           /_/    /_/
  |  /_/_/_/    /_/   /_/  /_/_/_/  |    _/_/    /_/  /_/_/_/_/    |
    /_/    _/  /_/   /_/  /_/    _/  /_/_/_/_/  /_/    /_/       - * -
   /_/    _/  /_/   /_/  /_/    _/  /_/        /_/    /_/          |
  /_/_/_/      _/_/_/   /_/_/_/_/   /_/_/_/   /_/    /_/_/
 /_/              _/
/_/     |     /_/_/    %s
      \033[94m- * -
        |\033[0m
\033[94m%s
%s\033[0m\n\n
""" % (VERSION_STRING, SAYING.strip(), CLONE_LINK)

# Path the the search results from a dork scan
DORK_SCAN_RESULTS_PATH = r"{}\lib\core\dork_check\scan_results".format(os.getcwd())

# Error message for when Google blocks your IP address
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE = "\nYou have been temporarily blocked from running Google searches."
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += " As of now there is no way around this. You will need to:\n"
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += "\tA) Change your IP address.\n"
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += "\tB) Wait about an hour for Google to lift the ban.\n"
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += "\tC) Manually check your Dorks.\n"
GOOGLE_TEMP_BLOCK_ERROR_MESSAGE += "\tD) Curse my name and this program"

# List of reserved port numbers, these are the ports that you want to check
RESERVED_PORTS = {
    1, 5, 7, 18, 20, 21, 22, 23, 25, 29, 37, 42, 43, 49,
    53, 69, 70, 79, 80, 103, 108, 109, 110, 115, 118, 119, 137, 139,
    143, 150, 156, 161, 179, 190, 194, 197, 389, 396, 443, 444, 445, 458,
    546, 547, 563, 569, 1080
}

# Links to some wordlists I have laying around
WORDLIST_LINKS = [
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrL2FhODgyMDk5ZWQxYzNlZjAwNWYzYWY2ZjhmYmFhZTExL3Jhdy84ODQ4NjBhNjAzZWQ0MjE3MTgyN2E1MmE3M2VjNzAzMjNhOGExZWY5L2dpc3RmaWxlMS50eHQ=',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrLzAwNWU3OWQ2NmU2MzA2YWI0MzZjOGJmYTc1ZTRiODMwL3Jhdy8xNjY5YjNjMDFmMjRhM2Q2OTMwZDNmNDE1Mjk3ZTg5OGQ1YjY2NGUzL29wZW53YWxsXzMudHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrLzE4NTBmM2EwZGNjNDE0YWZlOGM3NjYyMjBlOTYxYjE4L3Jhdy9iYWQ0NTA0NjcwY2FmM2UxNDY1NWI2ZjJlZGQ0MjJmOTJjMzI2MWI5L215c3BhY2UudHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrLzBkYWU2YTI5MjgzMjcyNmE2Y2MyN2VlNmVjOTdmMTFjL3Jhdy84MWFkOWFkOWUwZjQxMmY2YjIwMTM3MDI2NDcxZGRmNDJlN2JjMjkyL2pvaG4udHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrL2Q4ZjZiYjE2MGEzYzY2YzgyNWEwYWY0NDdhMDM1MDVhL3Jhdy83MWI4NmM5MGU3NDRkZjM0YzY3ODFjM2U0MmFjMThkOGM4ZjdkYjNlL2NhaW4udHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrL2JmM2MwYjQwMTVlYzlkMzY4YzBlNTczNzQ0MTAzYmU1L3Jhdy9lNzBhMThmOTUwNGYwZmMyYjRhMWRmN2M0Mjg2YjcyOWUyMzQ5ODljL29wZW53YWxsXzIudHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrLzQ1ZTExZDBhMzNjZGE1YjM3NDM5OGYyMDgxYjEwZWZiL3Jhdy8wNzQ1ZGMzNjFlZDU5NjJiMjNkYjUxM2FkOWQyOTNlODk0YjI0YTY0L2RjLnR4dA==',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrLzNmMzcxMWUzMDdlOGM0ZTM0MDkzYzI1OGFkN2UzZWZkL3Jhdy9hMjNiYmM3YTgxNTZhOGU5NTU3NmViYTA3MmIwZDg4ZTJmYjk1MzZiL2dtYWlsXzIudHh0',
    'aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9Fa3VsdGVrL2U3MzE4MGM3MGZmMzY3NDFhM2M4NzIzMDZiNTFhOTU1L3Jhdy9jODE0YjFjOTZiNGJkYzZlYTRlZDE3MmMzNDIwOTg2NTBjOTcyYWZjL2J0NC50eHQ='
]


def create_random_filename():
    """ Create a random file name
    >>> print(create_random_filename())
    56558c08-ee1f-40b4-b048-be4c4066f8b6 """
    return str(uuid.uuid4())


def decode64(string):
    """ Decode a string from base64 """
    return base64.b64decode(string)


def prompt(question):
    """ Ask a question.. """
    return raw_input("[{} PROMPT] {}".format(time.strftime("%I:%M:%S"), question))


def create_wordlist(b64link):
    """ Create a word list from a base64encoded URL by decoding it and connecting to it"""
    path = "{}/lib/text_files/wordlist.txt".format(PATH)
    data = urllib2.urlopen(base64.b64decode(b64link)).read()
    open(path, "w").close()
    with open(path, 'a+') as wordlist:
        for word in data:
            wordlist.write(word)
    return
