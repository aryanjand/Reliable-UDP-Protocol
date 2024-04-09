import socket
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
class UDPProxy:
    def __init__(self, client_address, server_address, proxy_address, stats, proxy_port, server_port, drop_prob, delay_prob, ack_drop_prob):
        self.client_address = client_address
        self.server_address = server_address
        self.stats = stats
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.drop_prob = drop_prob
        self.delay_prob = delay_prob
        self.ack_drop_prob = ack_drop_prob
        self.proxy_port = proxy_port
        self.proxy_address = proxy_address
    
    # Call if packet is from client, use % chance to drop and delay and forward the packet to server if chance > chance to drop/delay
    # If delay needed, generate random value in range
    def forward_from_client_to_server(self, data):
        pass  # Implement forwarding data from client to server
        packet_type = "ACK" if len(data) == 4 else "Data"
        drop_chance = self.ack_drop_prob if packet_type == "ACK" else "drop_prob"
        if drop_chance > random.random:
           print (f"Dropped a {packet_type} packet")
           self.stats ["packets_dropped"] += 1
           return
        delay = random.uniform(0,2) if self.delay_prob > random.random else 0 
        time.sleep(delay)
        self.sock.sendto(data.encode(), self.client_address)
        self.stats ["packets_dropped"] += 1
        print (f"Forwarded a {packet_type} packet after {delay:. 2f} s delay")

    # Call if packet is from server, use % chance to drop and delay and forward the packet to client if chance > chance to drop/delay
    # If delay needed, generate random value in range
    def forward_from_server_to_client(self, data):
        pass  # Implement forwarding data from server to client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self.server_port))
        self.server_address = (self.)

# Example usage
if __name__ == "__main__":
    proxy = UDPProxy("localhost", "localhost", 12345)
    data = "Hello, server!"
    proxy.forward_from_client_to_server(data)
