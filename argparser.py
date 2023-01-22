import argparse


def get_path_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='File name or absolute path to config file', required=True)
    namespace = parser.parse_args()
    return namespace.path
