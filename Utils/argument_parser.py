from argparse import Namespace, ArgumentParser, ArgumentTypeError
from socket import error, inet_aton


def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def non_negative_int(value):
    ivalue = int(value)
    if ivalue < 0:
        raise ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def valid_ip_address(value):
    try:
        inet_aton(value)
        return value
    except error:
        raise ArgumentTypeError("%s is not a valid IP address" % value)


def non_negative_float(value):
    fvalue = float(value)
    if fvalue < 0:
        raise ArgumentTypeError("%s is an invalid non-negative float value" % value)
    return fvalue


def valid_file_append_mode(value):
    if value.lower() not in ["a", "ab"]:
        raise ArgumentTypeError(
            f"{value} is not a valid file mode. Valid modes are 'Append' and 'Append binary'."
        )
    return value.lower()


def valid_file_read_mode(value):
    if value.lower() not in ["r", "rb"]:
        raise ArgumentTypeError(
            f"{value} is not a valid file mode. Valid modes are 'Read' and 'Read binary'."
        )
    return value.lower()


def _client_parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "ip_address", type=valid_ip_address, help="IP address of the server"
    )
    parser.add_argument("port", type=positive_int, help="Port number of the server")
    parser.add_argument("file_path", type=str, help="Path to the file")
    parser.add_argument(
        "--file_mode",
        type=valid_file_read_mode,
        default="r",
        help="File mode for opening the file (Read (r) or Read binary (rb))",
    )
    return parser.parse_args()


def _proxy_parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Process some integers.")

    parser.add_argument(
        "proxy_ip_address", type=valid_ip_address, help="IP address of the proxy"
    )
    parser.add_argument(
        "proxy_port", type=positive_int, help="Port number of the proxy"
    )
    parser.add_argument(
        "server_ip_address", type=valid_ip_address, help="IP address of the server"
    )
    parser.add_argument(
        "server_port", type=positive_int, help="Port number of the server"
    )

    parser.add_argument(
        "--client_drop",
        type=non_negative_float,
        default=0.5,
        help="Probability of dropping a client packet",
    )
    parser.add_argument(
        "--server_drop",
        type=non_negative_float,
        default=0.5,
        help="Probability of dropping a server packet",
    )
    parser.add_argument(
        "--client_delay_chance",
        type=non_negative_float,
        default=0.5,
        help="Probability of delaying a client packet",
    )
    parser.add_argument(
        "--server_delay_chance",
        type=non_negative_float,
        default=0.5,
        help="Probability of delaying a server packet",
    )
    parser.add_argument(
        "--client_delay_range",
        nargs=2,
        type=non_negative_int,
        default=(2, 3),
        help="Range for client packet delay",
    )
    parser.add_argument(
        "--server_delay_range",
        nargs=2,
        type=non_negative_int,
        default=(4, 5),
        help="Range for server packet delay",
    )

    return parser.parse_args()


def _server_parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "ip_address", type=valid_ip_address, help="IP address of the server"
    )
    parser.add_argument("port", type=positive_int, help="Port number of the server")
    parser.add_argument(
        "--file_mode",
        type=valid_file_append_mode,
        default="a",
        help="File mode for opening the file (Append (a) or Append binary (ab))",
    )
    return parser.parse_args()


def proxy_parse_arguments():
    args = _proxy_parse_arguments()
    return (
        args.proxy_ip_address,
        args.proxy_port,
        args.server_ip_address,
        args.server_port,
        args.client_drop,
        args.server_drop,
        args.client_delay_chance,
        args.server_delay_chance,
        args.client_delay_range,
        args.server_delay_range,
    )


def server_parse_arguments():
    args = _server_parse_arguments()
    return (args.ip_address, args.port, args.file_mode)


def client_parse_arguments():
    args = _client_parse_arguments()
    return (args.ip_address, args.port, args.file_path, args.file_mode)
