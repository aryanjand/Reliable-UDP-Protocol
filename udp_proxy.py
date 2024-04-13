from UDPNetworking.UnreliableProxy import UDPProxy
import threading

if __name__ == "__main__":
    print("Proxy Started\n")

    proxy = UDPProxy(
        0.0,
        1.0,
        1.0,
        0.0,
        (2, 3),
        (2, 3),
        ("127.0.0.1", 8000),
        ("127.0.0.1", 8080),
    )
    proxy.bind()
    address: tuple
    data_bytes: bytes
    data_bytes, address = proxy.get_client_request()
    print(f"Client Address: {address}")
    while True:
        thread = threading.Thread(
            target=proxy.unreliable_forward, args=(data_bytes, address)
        )
        thread.start()
        data_bytes, address = proxy.udp_socket.recvfrom()
