from argparse import Namespace, ArgumentParser


def client_parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Process some integers.")
    parser.add_argument("ip_address", type=str, help="IP address of the server")
    parser.add_argument("port", type=int, help="Port number of the server")
    parser.add_argument("file_path", type=str, help="Path to the file")
    return parser.parse_args()


def proxy_parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Process some integers.")

    parser.add_argument("proxy_ip_address", type=str, help="IP address of the proxy")
    parser.add_argument("proxy_port", type=int, help="Port number of the proxy")
    parser.add_argument("server_ip_address", type=str, help="IP address of the server")
    parser.add_argument("server_port", type=int, help="Port number of the server")

    parser.add_argument(
        "--client_drop",
        type=float,
        default=0.0,
        help="Probability of dropping a client packet",
    )
    parser.add_argument(
        "--server_drop",
        type=float,
        default=1.0,
        help="Probability of dropping a server packet",
    )
    parser.add_argument(
        "--client_delay_chance",
        type=float,
        default=1.0,
        help="Probability of delaying a client packet",
    )
    parser.add_argument(
        "--server_delay_chance",
        type=float,
        default=0.0,
        help="Probability of delaying a server packet",
    )
    parser.add_argument(
        "--client_delay_range",
        nargs=2,
        type=int,
        default=(2, 3),
        help="Range for client packet delay",
    )
    parser.add_argument(
        "--server_delay_range",
        nargs=2,
        type=int,
        default=(2, 3),
        help="Range for server packet delay",
    )

    return parser.parse_args()


def server_parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Process some integers.")
    parser.add_argument("ip_address", type=str, help="IP address of the server")
    parser.add_argument("port", type=int, help="Port number of the server")
    return parser.parse_args()
