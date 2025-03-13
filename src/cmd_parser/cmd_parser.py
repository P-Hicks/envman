
import argparse

def default_addition_of_args(parser):
    parser.add_argument('--no-confirmation', default=False, type=bool)


def init_arg_parser():
    parser = argparse.ArgumentParser(description="Environment Manager")
    default_addition_of_args(parser)
    # Define subparsers for commands
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    return parser, subparsers
