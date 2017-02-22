import os
from cmd import Cmd
from urllib2 import HTTPError
from lib.core.settings import LOGGER
from lib.core.settings import QUERY_REGEX


class PybeltConsole(Cmd):

    def do_run(self, command):
        """ Make your choice of what you want to do:
    - sqli
    - dork
    - xss
    - hashVerify
    - hashCrack
    - port
    - proxies
After you decide what you want to do type: run <command> """
        commands_list = ["sqli", "xss", "port", "hashCrack",
                         "hashVerify", "dork", "proxies"]

        if len(command) == 0:
            print("You have not supplied any command, available commands: {}".format(', '.join(
                commands_list
            )))
        elif command.lower() == "sqli":
            from lib.pointers import run_sqli_scan
            host = raw_input("Enter a host to scan for SQLi vulnerabilities: ")
            run_sqli_scan(host)
        elif command.lower() == "dork":
            from lib.pointers import run_dork_checker
            dork = raw_input("Enter a dork to scan with: ")
            run_dork_checker(dork)
        elif command.lower() == "xss":
            from lib.pointers import run_xss_scan
            host = raw_input("Enter a host to check XSS vulnerabilities on: ")
            proxy = raw_input("Enter a proxy to user (enter for none): ")
            user_agent = raw_input("Enter a user agent to spoof (enter for none): ")
            if proxy == "":
                proxy = None
            if user_agent == "":
                user_agent = None
            run_xss_scan(host, proxy=proxy, user_agent=user_agent)
        elif command.lower() == "hashverify":
            from lib.pointers import run_hash_verification
            h = raw_input("Enter a hash to verify: ")
            run_hash_verification(h)
        elif command.lower() == "hashcrack":
            from lib.pointers import run_hash_cracker
            h = raw_input("Enter a hash to crack: ")
            t = raw_input("Enter what type (all for none): ")
            full_data = h + ":" + t
            run_hash_cracker(full_data)
        elif command.lower() == "port":
            from lib.pointers import run_port_scan
            host = raw_input("Enter a host to scan open ports on: ")
            run_port_scan(host)
        elif command.lower() == "proxies":
            from lib.pointers import run_proxy_finder
            run_proxy_finder()
        else:
            print("{} is not a valid command. Valid commands are: {}".format(command, ', '.join(commands_list)))

    @staticmethod
    def do_quit():
        """ Terminate your running session """
        exit(0)
