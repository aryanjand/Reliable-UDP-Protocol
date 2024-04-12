from UDPNetworking.UnreliableProxy import UDPProxy
import argparse

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
