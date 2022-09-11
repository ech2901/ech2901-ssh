from socket import socket

class TransportHandler(object):
    def __init__(self, server, client: socket):

        self.server = server
        self.client = client

        self.get_client_version()
        self.exchange_protocols()


    def get_client_version(self):
        # TODO: handle preamble comments
        self.client_version = self.client.recv(255).decode()
        self.client.send(self.server.version_exchange.encode())

    def exchange_protocols(self):
        # TODO: Send server acceptable protocols
        self.client_protocols = self.client.recv(2048)

    def __repr__(self):
        out = f'Client Version: {self.client_version}'
        out = f'{out}Client Protocols: {self.client_protocols}'
        return out

