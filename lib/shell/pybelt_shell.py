from cmd import Cmd

from lib.core.settings import TOOL_LIST


class PybeltConsole(Cmd):

    """ Interactive shell that will launch if you fail to pass a flag """

    @staticmethod
    def help_menu():
        """
        Specs: Produce a help menu with basic descriptions
        Usage: run menu
        """
        print("\t  Command    Descriptor")
        for key in TOOL_LIST.iterkeys():
            print("""
            {}       {}""".format(key, TOOL_LIST[key]))

    def do_run(self, command):
        """
        Specs: Run one of the tools by their hyphened name
        Usage: run [tool-hyphen]
        """

        if len(command) == 0:
            print("You have not supplied any command, available commands: {}".format(', '.join(
                TOOL_LIST
            )))
        elif command.lower() == "-s":
            from lib.pointers import run_sqli_scan
            host = raw_input("Enter a host to scan for SQLi vulnerabilities: ")
            run_sqli_scan(host)
        elif command.lower() == "-d":
            from lib.pointers import run_dork_checker
            dork = raw_input("Enter a dork to scan with: ")
            run_dork_checker(dork)
        elif command.lower() == "-x":
            from lib.pointers import run_xss_scan
            host = raw_input("Enter a host to check XSS vulnerabilities on: ")
            proxy = raw_input("Enter a proxy to user (enter for none): ")
            user_agent = raw_input("Enter a user agent to spoof (enter for none): ")
            if proxy == "":
                proxy = None
            if user_agent == "":
                user_agent = None
            run_xss_scan(host, proxy=proxy, user_agent=user_agent)
        elif command.lower() == "-v":
            from lib.pointers import run_hash_verification
            h = raw_input("Enter a hash to verify: ")
            run_hash_verification(h)
        elif command.lower() == "-h":
            from lib.pointers import run_hash_cracker
            h = raw_input("Enter a hash to crack: ")
            t = raw_input("Enter what type (all for none): ")
            if t is None or t == "":
                t = "all"
            full_data = h + ":" + t
            run_hash_cracker(full_data)
        elif command.lower() == "-p":
            from lib.pointers import run_port_scan
            host = raw_input("Enter a host to scan open ports on: ")
            run_port_scan(host)
        elif command.lower() == "-f":
            from lib.pointers import run_proxy_finder
            run_proxy_finder()
        elif command.lower() == "-hh":
            self.help_menu()
        else:
            print("{}".format(self.help_menu()))

    def do_quit(self, line):
        """ Terminate your running session """
        print("[*] Terminating session..")
        exit(0)
