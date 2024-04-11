import argparse
from UDPNetworking.UnreliableProxy import UnrealiableProxy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proxy")
    parser.add_argument("client_address", help="IP address of the client")
    parser.add_argument("client_port", type=int, help="Port of the client")
    parser.add_argument("server_port", type=int, help="Port of the server")
    parser.add_argument("server_address", help = "IP address of the server")
    parser.add_argument("proxy_address",help = "IP address of the proxy")
    parser.add_argument("proxy_port",type = int, help = "Port of the proxy")
    parser.add_argument("drop_prob", type=float, help="Probability to drop data packets")
    parser.add_argument("delay_prob", type=float, help="Probability to delay packets")
    parser.add_argument("ack_drop_prob", type=float, help="Probability to drop ACK packets")
    parser.add_argument("stats_file", help="File to save statistics")
    args = parser.parse_args()
    proxy = UnrealiableProxy(args.client_address, args.client_port, args.server_address, args.server_port, args.proxy_port, args.proxy_address, args.drop_prob, args.delay_prob, args.ack_drop_prob)