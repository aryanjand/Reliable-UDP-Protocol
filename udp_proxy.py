from UDPNetworking.UnreliableProxy import UDPProxy
from Utils.argument_parser import proxy_parse_arguments
import threading

if __name__ == "__main__":
    print("Proxy Started\n")
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

    client_delay_min, client_delay_max = client_delay_range
    server_delay_min, server_delay_max = server_delay_range

    proxy = UDPProxy(
        0.0,
        1.0,
        1.0,
        0.0,
        (2, 3),
        (2, 3),
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
