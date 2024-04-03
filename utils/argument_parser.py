import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('ip_address', type=str, help='IP address of the server')
    parser.add_argument('port', type=int, help='Port number of the server')
    parser.add_argument('file_path', type=str, help='Path to the file')
    return parser.parse_args()
