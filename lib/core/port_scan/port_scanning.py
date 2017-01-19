import socket
from lib.core.settings import LOGGER
from lib.core.settings import RESERVED_PORTS


class PortScanner(object):

    connection_made = []  # Connection made in list form

    def __init__(self, host):
        self.host = host
        self.ports = RESERVED_PORTS

    def connect_to_host(self):
        """ Attempt to make a connection using the most common ports 443, 445, etc.. """
        host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in self.ports:
            try:
                LOGGER.info("Attempting to connect to port: {}".format(port))
                attempt = host.connect_ex((self.host, port))  # Connect to the host
                if attempt:  # If connection fails
                    pass
                else:
                    self.connection_made.append(port)
            except socket.error:
                pass
        host.close()
        if not self.connection_made:
            LOGGER.fatal("No connections could be made.")
        else:
            return "Connection made on port: {}.".format(''.join(str(self.connection_made)))
