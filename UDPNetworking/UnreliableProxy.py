from Model.UDPSocket import UDPSocket
from typing import Tuple
import random
import time
from datetime import timedelta

CLIENT = 0
SERVER = 1


class ProxyConfig:
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
        self.config = ProxyConfig(
            client_drop,
            server_drop,
            client_delay_chance,
            server_delay_chance,
            client_delay_range,
            server_delay_range,
            server_address,
            proxy_address,
        )
        self.udp_socket: UDPSocket = UDPSocket()
        self.client_address = None
        self.start_time = time.perf_counter()
        print(self.start_time)
        self.packets_received_timestamped = []
        self.packets_received = 0
        self.packets_dropped_timestamped = []
        self.packets_dropped = 0
        self.packets_delayed_timestamped = []
        self.packets_delayed = 0
        self.packets_sent_timestamped = []
        self.packets_sent = 0

    def bind(self) -> None:
        self.udp_socket.bind(self.config.proxy_address)
        return

    def get_client_request(self) -> Tuple[bytes, tuple]:
        bytes_received, client_address = self.udp_socket.recvfrom()
        self.client_address = client_address
        self.packets_received += 1
        self.packets_received_timestamped.append((timedelta(seconds=time.perf_counter()-self.start_time).total_seconds(), self.packets_received))
        return (bytes_received, client_address)

    def unreliable_forward(self, data, address: tuple) -> None:
        forward_address, destination = self.get_forward_address(address)
        self.packets_received += 1
        self.packets_received_timestamped.append((timedelta(seconds=time.perf_counter()-self.start_time).total_seconds(), self.packets_received))
        if self.should_drop_packet(destination):
            print(
                f"Packet dropped from {address} ({'Server' if destination != SERVER else 'Client'})"
            )
            self.packets_dropped += 1
            self.packets_dropped_timestamped.append((timedelta(seconds=time.perf_counter()-self.start_time).total_seconds(), self.packets_dropped))
            return
        if self.should_delay_packet(destination):
            print(
                f"Packet delayed from {address} ({'Server' if destination != SERVER else 'Client'})"
            )
            self.packets_delayed += 1
            self.packets_delayed_timestamped.append((timedelta(seconds=time.perf_counter()-self.start_time).total_seconds(), self.packets_delayed))
            self.delay_packet(destination)
        print(
            f"Forwarding packet from {address} ({'Server' if destination != SERVER else 'Client'}) "
            f"to {forward_address} ({'Server' if destination == SERVER else 'Client'})"
        )
        self.packets_sent += 1
        self.packets_sent_timestamped.append((timedelta(seconds=time.perf_counter()-self.start_time).total_seconds(), self.packets_sent))
        self.udp_socket.sendto(data, forward_address)
        return

    def delay_packet(self, destination: tuple) -> None:
        time.sleep(self.get_delay_time(destination))
        return

    def should_drop_packet(self, destination: int) -> bool:
        return random.random() < (
            self.config.server_drop
            if destination != SERVER
            else self.config.client_drop
        )

    def should_delay_packet(self, destination: int) -> bool:
        return random.random() < (
            self.config.server_delay_chance
            if destination != SERVER
            else self.config.client_delay_chance
        )

    def get_delay_time(self, destination: int) -> float:
        return (
            random.uniform(
                self.config.server_delay_range[0], self.config.server_delay_range[1]
            )
            if destination != SERVER
            else random.uniform(
                self.config.client_delay_range[0], self.config.client_delay_range[1]
            )
        )

    def get_forward_address(self, address: tuple) -> Tuple[tuple, int]:
        return (
            (self.config.server_address, SERVER)
            if self.client_address == address
            else (self.client_address, CLIENT)
        )
