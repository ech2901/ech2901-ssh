from socket import socket
from .Packets import *


class TransportHandler(object):
    def __init__(self, server: socket, client: socket):

        self.server = server
        self.client = client

        self.get_client_version()

        self.buffer = b''


    def get_client_version(self):
        # TODO: handle preamble comments
        self.client_version = self.client.recv(255).decode()
        self.client.send(self.server.version_exchange.encode())

    def get_packet(self):
        data = self.buffer + self.client.recv(2048)
        packet, self.buffer = Packet.decode(data)
        return packet

    def send_packet(self, packet: Packet):
        print(packet.encode())
        self.client.send(packet.encode())

    def exchange_protocols(self):
        # TODO: Send server acceptable protocols
        self.client_protocols = self.client.recv(2048)

    def __repr__(self):
        out = f'Client Version: {self.client_version}'
        out = f'{out}Client Protocols: {self.client_protocols}'
        return out

