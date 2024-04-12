from UDPNetworking.UnreliableProxy import UDPProxy
import threading

if __name__ == "__main__":
    print("Proxy Started\n")

    proxy = UDPProxy(
        0.5,
        0.5,
        0.5,
        0.5,
        (1000, 3000),
        (1000, 3000),
        ("localhost", 8000),
        ("localhost", 8080),
    )
    proxy.bind()
    address: tuple
    data_bytes: bytes
    data_bytes, address = proxy.get_client_request()

    while True:
        thread = threading.Thread(
            target=proxy.unreliable_forward, args=(data_bytes, address)
        )
        data_bytes, address = proxy.socket.recvfrom()
