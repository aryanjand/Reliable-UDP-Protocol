from UDPNetworking.UnreliableProxy import UDPProxy
from Utils.argument_parser import proxy_parse_arguments
import threading
import time
import matplotlib.pyplot as plt


if __name__ == "__main__":
    try:
        (
            proxy_ip,
            proxy_port,
            server_ip,
            server_port,
            client_drop,
            server_drop,
            client_delay_chance,
            server_delay_chance,
            client_delay_range,
            server_delay_range,
        ) = proxy_parse_arguments()
        print("Proxy Started\n")

        client_delay_min, client_delay_max = client_delay_range
        server_delay_min, server_delay_max = server_delay_range

        proxy = UDPProxy(
            client_drop,
            server_drop,
            client_delay_chance,
            server_delay_chance,
            client_delay_range,
            server_delay_range,
            (server_ip, server_port),
            (proxy_ip, proxy_port),
        )
        proxy.bind()
        data_bytes, address = proxy.get_client_request()
        print(f"Client Address: {address}")
        while True:
            thread = threading.Thread(
                target=proxy.unreliable_forward, args=(data_bytes, address)
            )
            thread.start()
            data_bytes, address = proxy.udp_socket.recvfrom()
    finally:
        delayed_packet_nums = []
        delayed_packet_timestamps = []
        for packet in proxy.packets_delayed_timestamped:
            print("Delayed packets ", packet)
            delayed_packet_nums.append(packet[1])
            delayed_packet_timestamps.append(packet[0])
        dropped_packet_nums = []
        dropped_packet_timestamps = []
        for packet in proxy.packets_dropped_timestamped:
            print("Dropped packets ", packet)
            dropped_packet_nums.append(packet[1])
            dropped_packet_timestamps.append(packet[0])
        received_packet_nums = []
        received_packet_timestamps = []
        for packet in proxy.packets_received_timestamped:
            print("Packets received ", packet)
            received_packet_nums.append(packet[1])
            received_packet_timestamps.append(packet[0])
        sent_packet_nums = []
        sent_packet_timestamps = []
        for packet in proxy.packets_sent_timestamped:
            print("Packets sent ", packet)
            sent_packet_nums.append(packet[1])
            sent_packet_timestamps.append(packet[0])
        plt.plot(sent_packet_timestamps, sent_packet_nums, label="Packets Sent")
        plt.plot(dropped_packet_timestamps, dropped_packet_nums, label="Packets Dropped")
        plt.plot(delayed_packet_timestamps, delayed_packet_nums, label="Packets Delayed")
        plt.plot(received_packet_timestamps, received_packet_nums, label="Packets Received")
        plt.xlabel('Time since start')
        plt.ylabel('Number of packets')
        plt.legend(loc="upper left")
        plt.show()
