from Model.UDPSocket import UDPSocket
from Utils.serializer import serialize, deserialize
import random
import time

# TODO
# Implement proxy
# Options needed: % Chance to drop packets from client
#                 % Chance to drop packets from server
#                 % Chance to add delay to client packets
#                 % Chance to add delay to server packets
#                 Range (min/max) in milliseconds to delay a packet from client
#                 Range (min/max) in milliseconds to delay a packet from server
# Parse the options and operate as necessary

CLIENT = 0
SERVER = 1


class UDPProxy:
    def __init__(
        self,
        client_drop: float,
        server_drop: float,
        client_delay_chance: float,
        server_delay_chance: float,
        client_delay_range: tuple,
        server_delay_range: tuple,
        server_address: tuple,
        proxy_address: tuple,
    ):
        self.client_drop = client_drop
        self.server_drop = server_drop
        self.client_delay_chance = client_delay_chance
        self.server_delay_chance = server_delay_chance
        self.client_delay_range = client_delay_range
        self.server_delay_range = server_delay_range
        self.server_address = server_address
        self.proxy_address = proxy_address
        self.client_address = None
        self.socket: UDPSocket = UDPSocket()

    def bind(self):
        self.socket.bind(self.proxy_address)

    def get_client_request(self) -> bytes:
        bytes_received, client_address = self.socket.recvfrom()
        self.client_address = client_address
        return (bytes_received, client_address)

    def unreliable_forward(self, data, address: tuple):
        forward_address = self.get_forward_address(address)
        if self.should_drop_packet(address):
            return
        if self.should_delay_packet(address):
            self.delay_packet(data, forward_address)
        else:
            self.socket.sendto(data, forward_address)

    def delay_packet(self, address: tuple):
        if self.should_delay_packet(address):
            time.sleep(self.get_delay_time(address))

    def send_client_or_server(self, client_or_server: str, data: bytes):
        self.socket.sendto(
            data,
            (
                self.server_address
                if client_or_server == "server"
                else self.client_address
            ),
        )

    def should_drop_packet(self, address: tuple) -> bool:
        return random.random() < (
            self.server_drop if address == self.server_address else self.client_drop
        )

    def should_delay_packet(self, address: tuple) -> bool:
        return random.random() < (
            self.server_delay_chance
            if address == self.server_address
            else self.client_delay_chance
        )

    def get_delay_time(self, address: tuple):
        return (
            random.uniform(self.client_delay_range[0], self.client_delay_range[1])
            if address == self.client_address
            else random.uniform(self.server_delay_range[0], self.server_delay_range[1])
        )

    def get_forward_address(self, address: tuple) -> tuple:
        return (
            self.server_address
            if self.client_address == address
            else self.client_address
        )
