import socket
from lib.core.settings import RESERVED_PORTS
from lib.core.settings import PORT_DESCRIPTIONS


class PortScanner(object):

    def __init__(self, host):
        self.host = host
        self.ports = RESERVED_PORTS

    def connect_to_host(self):
        host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connections_made = None
        for port in self.ports:
            try:
                print("Checking port {}.".format(port))
                host.connect_ex((self.host, port))
                if True:
                    connections_made = [port]
                    continue
            except socket.error:
                pass
        if not connections_made:
            return "\nNo connections could be made."
        else:
            return "\nConnections made on port: {}, description: {}".format(connections_made,
                                                                            PORT_DESCRIPTIONS[str(connections_made)])
