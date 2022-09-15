from SSH_Core import Byte, Boolean, UInt32, UInt64, String, MPInt, NameList
from random import randint
from os import urandom
from struct import unpack


class Packet(object):


    @classmethod
    def decode(cls):



    def encode(self, cipher_size=0, mac_len=0):
        padding_mod = cipher_size if cipher_size else 8
        random_size = randint(4, 255)
        if random_size > 127:
            random_size = random_size - ((self.packet_length.data + random_size) % padding_mod)
        else:
            pass

