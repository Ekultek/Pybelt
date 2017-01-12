import random
import os
import uuid
import re
import logging
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
VERSION = "1.0"

# Coloring for the version string
TYPE_COLORS = {"dev": 33, "stable": 92}

# Type of version that the program is in "dev" or "stable"
VERSION_STRING = "\033[92m{}\033[0m(\033[{}m\033[1mdev\033[0m)".format(VERSION, TYPE_COLORS["dev"]) if len(VERSION) >= 4 else \
    "\033[92m{}\033[0m(\033[{}m\033[1mstable\033[0m)".format(VERSION, TYPE_COLORS["stable"])

# Clone link
CLONE_LINK = "https://github.com/ekultek/pybelt.git"

# Basic legal disclaimer
LEGAL_DISC = "legal disclaimer: This program is intended for learning purposes, any malicious intent is on you, it is the end users responsibility to obey all laws, regulations, and rules of your respective country or place of origin. For further information about this please see the legal information file under docs or run the --legal flag"

# Random dork to use for basic sqli searches
RANDOM_DORK = random.choice(open("{}/lib/core/text_files/dorks.txt".format(PATH)).readlines())

# Random saying to display on the banner
RANDOM_SAYING = random.choice(open("{}/lib/core/text_files/sayings.txt".format(PATH)).readlines())

# Random common column names
RANDOM_COMMON_COLUMN = random.choice(open("{}/lib/core/text_files/common_columns.txt".format(PATH)).readlines())

# Search query regex to make sure the URLS have a GET parameter
QUERY_REGEX = re.compile(r"(.*)[?|#](.*){1}\=(.*)")

SQLI_ERROR_REGEX = (
    re.compile(r"SQL syntax.*MySQL"),  # You have an error in your SQL syntax
    re.compile("Warning.*mysql_.*"),  # Warning MySQL syntax contains an error at line ..
    re.compile(r"valid MySQL result"),  # Your search has produced a invalid MySQL result
    re.compile(r"MySqlClient\."),  # You have an error located at .. in your MySQL client server
)

SYNTAX_REGEX = re.compile(r"\W+$")

# Sexy ass banner
BANNER = """
        \033[94m##### ##                    /              ###
     ######  /###                 #/                ###
    /#   /  /  ###                ##                 ##     #
   /    /  /    ###               ##                 ##    ##
       /  /      ##               ##                 ##    ##
      ## ##      ## ##   ####     ## /###     /##    ##  ########
      ## ##      ##  ##    ###  / ##/ ###  / / ###   ## ########
    /### ##      /   ##     ###/  ##   ###/ /   ###  ##    ##
   / ### ##     /    ##      ##   ##    ## ##    ### ##    ##
      ## ######/     ##      ##   ##    ## ########  ##    ##
      ## ######      ##      ##   ##    ## #######   ##    ##
      ## ##          ##      ##   ##    ## ##        ##    ##
      ## ##          ##      ##   ##    /# ####    / ##    ##
      ## ##           #########    ####/    ######/  ### / ##
 ##   ## ##             #### ###    ###      #####    ##/   ##
###   #  /                    ###
 ###    /              #####   ###
  #####/             /#######  /#
    ###             /      ###/\033[0m      %s

\033[94m%s
%s\033[0m

\033[91m[!] %s\033[0m\n\n
""" % (VERSION_STRING, RANDOM_SAYING.strip(), CLONE_LINK, LEGAL_DISC)

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
    1, 5, 7, 18, 20, 21, 22, 23, 25, 29, 37,  42, 43, 49, 53, 69, 70,
    79, 80, 103, 108, 109, 110, 115, 118, 119, 137, 139, 143, 150, 156,
    161, 179, 190, 194, 197, 389, 396, 443, 444, 445, 458, 546, 547, 563,
    569, 1080
}


def create_random_filename():
    """ Create a random file name
    >>> print(create_random_filename())
    56558c08-ee1f-40b4-b048-be4c4066f8b6 """
    return str(uuid.uuid4())
