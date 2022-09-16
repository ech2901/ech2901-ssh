from SSH_Core import Byte, Boolean, UInt32, UInt64, String, MPInt, NameList
from SSH_Core.Numbers import TransportMessage

from dataclasses import dataclass
from random import randint
from os import urandom
from struct import unpack

@dataclass
class Packet(object):
    packet_len: UInt32
    padding_len: Byte[1]
    payload: Byte
    padding: Byte
    mac: Byte[0]

    @classmethod
    def decode(cls, data: bytes):
        output = dict()
        for key, data_type in cls.__annotations__.items():
            if key == 'payload':
                size = output['packet_len']-output['padding_len']-1
                output[key], data = data_type.decode(data, size)
            elif key == 'padding':
                output[key], data = data_type.decode(data, int(output['padding_len']))
            else:
                output[key], data = data_type.decode(data)
        return cls(**output), data

    def encode(self):
        output = b''
        for data in self.__dict__.values():
            output = output+data.encode()
        return output


@dataclass
class AlgoNegotiation(object):
    key_exchange_init: TransportMessage
    cookie: Byte[16]
    kex_algorithms: NameList
    server_host_key_algorithms: NameList
    encryption_algorithms_client_to_server: NameList
    encryption_algorithms_server_to_client: NameList
    mac_algorithms_client_to_server: NameList
    mac_algorithms_server_to_client: NameList
    compression_algorithms_client_to_server: NameList
    compression_algorithms_server_to_client: NameList
    languages_client_to_server: NameList
    languages_server_to_client: NameList
    first_kex_packet_follows: Boolean
    reserved: UInt32

    @classmethod
    def decode(cls, data: bytes):
        output = dict()
        for key, data_cls in cls.__annotations__.items():
            output[key], data = data_cls.decode(data)
        return cls(**output)




