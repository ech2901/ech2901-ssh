from SSH_Core import Byte, Boolean, UInt32, UInt64, String, MPInt, NameList
from dataclasses import dataclass
from random import randint
from os import urandom
from struct import unpack

@dataclass
class Packet(object):
    packet_len: UInt32
    padding_len: Byte
    payload: Byte
    padding: Byte
    mac: Byte

    @classmethod
    def decode(cls, data: bytes, mac_len=0):
        packet_length, data = UInt32.decode(data)
        padding_length, data = Byte.decode(data, 1)

        size = packet_length-padding_length-1
        payload, data = Byte.decode(data, size)
        random_padding, data = Byte.decode(data, int(padding_length))
        mac, data = Byte.decode(data, mac_len)

        return cls(packet_length, padding_length, payload, random_padding, mac), data


