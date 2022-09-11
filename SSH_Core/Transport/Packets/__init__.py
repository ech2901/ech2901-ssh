from struct import pack, unpack
from dataclasses import dataclass

@dataclass
class Packet(object):
    packet_length: int
    padding_length: int
    payload: bytes
    random_padding: bytes
    mac: bytes

    @classmethod
    def decode(cls, data):
        packet_length, padding_length = unpack('!IB', data[:5])
        payload = data[5:][:packet_length-padding_length]
        random_padding = data[5:][packet_length-padding_length: packet_length]
        mac = data[packet_length:]

        return cls(packet_length, padding_length, payload, random_padding, mac)


@dataclass
class AlgorithmNegotiation(object):
    SSH_MSG_KEXINIT = int
    cookie = bytes
    kex_algorithms