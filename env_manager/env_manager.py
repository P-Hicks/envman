import argparse
import os
import json
import re
import shutil


'''
TODO:
name current environment, be able to save without name
 * add hash of each to see if current
rename action?
configurable ask for confirmation
configs to thing like environment path and case sensitivity
'''
from src.actions.action_manager import setup_actions_as_subcommands, perform_command
from src.actions.concrete_actions import *
from src.cmd_parser.cmd_parser import init_arg_parser



def main():
    parser, subparser = init_arg_parser()
    setup_actions_as_subcommands(subparser)
    # parser = argparse.ArgumentParser(description="Environment Manager")
    # parser.add_argument('--no-confirmation', default=False, type=bool)
    # Define subparsers for commands
    # subparsers = parser.add_subparsers(dest="command", required=True)

    args = parser.parse_args()
    perform_command(args)
    
        
if __name__ == "__main__":
    if not os.path.exists(path_to_environment_data):
        os.mkdir(path_to_environment_data)
    main()
