import socket
import time
from lib.core.settings import LOGGER
from lib.core.settings import RESERVED_PORTS


class PortScanner(object):

    connection_made = []  # Connection made in list form

    def __init__(self, host):
        self.host = host
        self.ports = RESERVED_PORTS

    def connect_to_host(self):
        start_time = time.time()
        try:
            for port in RESERVED_PORTS.keys():
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                res = sock.connect_ex((self.host, port))
                if res == 0:
                    LOGGER.info("[*] Open: {}  {}".format(port, RESERVED_PORTS[port]))
                    self.connection_made.append(port)
                sock.close()
        except Exception, e:
            print e

        stop_time = time.time()
        LOGGER.info("Completed in {} seconds".format(str(stop_time - start_time)))
        LOGGER.info("Ports readily available: {}".format(''.join(str(self.connection_made))))
