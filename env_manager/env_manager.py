import argparse
import os
import json
import re
import shutil

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINKING = '\033[5m'
    BLACK	= '\033[90m'#	40
    RED	    = '\033[91m'#	41
    GREEN	= '\033[92m'#	42
    YELLOW	= '\033[93m'#	43
    BLUE	= '\033[94m'#	44
    MAGENTA	= '\033[95m'#	45
    CYAN	= '\033[96m'#	46
    WHITE	= '\033[97m'#	47
    DEFAULT	= '\033[99m'#	49
    LEFT_1	= '\033[#D'
def print_w_color(*args, **kwargs):
    color = kwargs.pop('color')
    args = list(args)
    if color is not None:
        args.insert(0, color)
        args.append(bcolors.ENDC)
    print(*args, *kwargs)

def input_w_color(prompt, **kwargs):
    color = kwargs.pop('color')
    if color is not None:
        prompt = color + prompt + bcolors.ENDC 
    return input(prompt, *kwargs)


'''
TODO:
adding y/n to confirm stuff
name current environment, be able to save without name
 * add hash of each to see if current
rename action?
configurable ask for confirmation
adding color
better docs and help information
better list of args
configs to thing like environment path and case sensitivity
'''

class EnvironmentVariable:
    def __init__(self, key = None, value = None, comment = None):
        self._key = key
        self._value = value
        self._comment = comment

class Environment:
    def __init__(self, name):
        self._name = name
        self._variables : list[EnvironmentVariable] = []

    def add_variable(self, var : EnvironmentVariable):
        self._variables.append(var)
        

def confirm_action(prompt : str, should_exit_on_no : bool = False) -> bool:
    confirmation = input_w_color(f'{prompt} (y/n) ', color = bcolors.MAGENTA)
    if confirmation == 'y' or confirmation == 'Y' or confirmation.lower() == 'yes':
        return True
    if should_exit_on_no:
        print('done.')
        exit(0)
    return False
    

def none_are_null(*args):
    for arg in args:
        if arg is None:
            return False
    return True
        
class EnvFileEnvironmentManager:
     
    def create_env_file_from_environment(self, path_to_env_file : str, env : Environment) -> str:
        env_str = self.create_env_str_from_environment(env)
        write_string_to_file(
            file_path=path_to_env_file,
            content=env_str,
        )
    
    
    def create_env_str_from_environment(self, env : Environment) -> str:
        env_list = [
            (
                # Write all 3 (key, value, comment) if none are null
                f'{var._key}="{var._value}"#{var._comment}' if none_are_null(var._key, var._value, var._comment,) \
                # One is null
                # if key and value are not null, only comment is null. write key value
                else f'{var._key}="{var._value}"' if none_are_null(var._key, var._value) \
                # either key or value or both are null.
                # if comment is not null, write comment
                else f'#{var._comment}"' if none_are_null(var._comment) \
                # all is null, blank line
                else ""
            )
            for var in env._variables
        ]
        env_str = '\n'.join(env_list)
        return env_str

    def parse_environment_from_env_file(self, env_name : str, path_to_env_file : str) -> Environment:
        env_str = read_file_to_string(path_to_env_file)
        return self.parse_environment_from_env_str(env_name, env_str)

    def parse_env_line(self, line: str):
        """
        CHATGPT
        Parses a line from a .env file into key, value, and comment.
        
        :param line: A single line from a .env file.
        :return: A tuple (key, value, comment) where each can be None if missing.
        """
        line = line.strip()
        
        if not line or line.startswith("#"):
            return None, None, line if line else None
        
        # old regex r'([^#=]+)?(?:\s*=\s*([^#]*))?(?:\s*#(.*))?'
        match = re.match(r'([^#=]+)?(?:\s*=\s*(["\']?.*?["\']?))?(?:\s+#(.*))?', line)
        
        if match:
            key = match.group(1).strip() if match.group(1) else None
            value = match.group(2).strip() if match.group(2) else None
            comment = match.group(3).strip() if match.group(3) else None
            return key, value, comment
        
        return None, None, None  # Fallback case
    
    def parse_environment_from_env_str(self, env_name : str, env_str : str) -> Environment:
        lines = env_str.split('\n')
        environment = Environment(name=env_name)
        for line in lines:
            key, value, comment = self.parse_env_line(line)
            if (value is not None) and ((value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'"))):
                # Removes quotes from string entries
                value = value[1:-1]
            environment.add_variable(
                EnvironmentVariable(
                    key = key,
                    value = value,
                    comment = comment,
                )
            )
        
        return environment



path_to_environment_data = '.development_environments'
is_case_sensitive = False
current_in_use_env_file_path = ".env"
example_env_file_path = "example.env"

def generate_path_to_env(env_name):
    if not is_case_sensitive:
        env_name = env_name.lower()
    file_path = f'{path_to_environment_data}/{env_name}.env'
    return file_path


def read_file_to_string(file_path : str) -> str:
    """Reads the entire content of a file into a string."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    
def write_string_to_file(file_path : str, content : str):
    """Writes a given string to a file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def init_env(args):
    """Initialize the environment with given arguments."""
    if os.path.exists(current_in_use_env_file_path):
        confirm_action(f"environment is already set, and will be overridden with default. are you sure?", should_exit_on_no=True)
    shutil.copy(
        src=example_env_file_path,
        dst=current_in_use_env_file_path,
    )
    
    
def load_env(args):
    """Load environment settings."""
    env_name = args[0]
    file_path = generate_path_to_env(env_name)
    if not os.path.exists(file_path ):
        print(f'envrionment {env_name} not set. cannot load.')
        exit(0)
    if os.path.exists(current_in_use_env_file_path):
        confirm_action(f"environment is already set, and will be overridden with default. are you sure?", should_exit_on_no=True)
    shutil.copy(
        dst=current_in_use_env_file_path,
        src=file_path,
    )
    # json_env = JsonFileEnvironmentManager().get_environment_from_json_file(file_path)
    # env_string = EnvFileEnvironmentManager().create_env_file_from_environment(
    #     path_to_env_file=current_in_use_env_file_path,
    #     env = json_env,
    # )
    
def save_env(args):
    """Save environment settings."""
    env_name = args[0]
    file_path = generate_path_to_env(env_name)
    if not os.path.exists(current_in_use_env_file_path):
        print(f'current envrionment not set. cannot load.')
        exit(0)
    if os.path.exists(file_path ):
        confirm_action(f"environment is already set, and will be overridden with current. are you sure?", should_exit_on_no=True)
    shutil.copy(
        dst=file_path,
        src=current_in_use_env_file_path,
    )
    # env = EnvFileEnvironmentManager().parse_environment_from_env_file(env_name, current_in_use_env_file_path)
    # json_str = JsonFileEnvironmentManager().write_json_file_from_environment(path_to_env_file=file_path, env=env)
    

def list_envs(args):
    envs = os.listdir(path_to_environment_data)
    env_file_ending = '.env'
    envs = [
        env for env in envs if env.endswith(env_file_ending)
    ]
    print(f'{len(envs)} development environments found...')
    for env in envs:
        env_name = env[0:-len(env_file_ending)]
        print(env_name)

def clear_env(args):
    if os.path.exists(current_in_use_env_file_path ):
        confirm_action(f"current environment is set, and will be deleted. are you sure?", should_exit_on_no=True)
    write_string_to_file(
        file_path=current_in_use_env_file_path,
        content=''
    )

def delete_env(args):
    env_name = args[0]
    file_path = generate_path_to_env(env_name=env_name)
    if not os.path.exists(file_path):
        print(f'envrionment {env_name} not set. cannot delete.')
        exit(0)
    if os.path.exists(file_path ):
        confirm_action(f"environment is set, are you sure you want to delete?", should_exit_on_no=True)
    os.remove(
        path=file_path
    )
    
def clearall_env(args):
    envs = os.listdir(path_to_environment_data)
    env_file_ending = '.env'
    confirm_action(f"are you sure you want to delete ALL saved environments?", should_exit_on_no=True)
    envs = [
        env for env in envs if env.endswith(env_file_ending)
    ]
    print(f'{len(envs)} development environments found...')
    for env in envs:
        print(f'removing {env}...')
        os.remove(f'{path_to_environment_data}/{env}')    
    

def read_env(args):
    env_name = args[0]
    file_path = generate_path_to_env(env_name=env_name)
    string = read_file_to_string(file_path=file_path)
    print(string)

def get_index_of_end_of_shared_prefix(str1: str,str2: str,):
    '''
    returns None if there is no end of shared prefix, returns 0 if no shared prefix
    '''
    i = 0
    len_1 = len(str1)
    len_2 = len(str2)
    min_len = min(len_1, len_2)
    while i < min_len and str1[i] == str2[i]:
        i = i + 1
    if i >= min_len:
        return None
    if str1[i] != str2[i]:
        return i
    return None

def compare_env(args):
    env_name_1 = args[0]
    env_name_2 = args[1]
    
    max_length = max(len(env_name_1), len(env_name_2), 4) + 1
    formatted_env_name_1 = env_name_1.ljust(max_length)
    formatted_env_name_2 = env_name_2.ljust(max_length)
    formatted_both = "both".ljust(max_length)
    
    file_path_1 = generate_path_to_env(env_name=env_name_1)
    string_1 = read_file_to_string(file_path=file_path_1)
    list_lines_1 = string_1.split('\n')
    list_lines_1.sort()
    
    file_path_2 = generate_path_to_env(env_name=env_name_2)
    string_2 = read_file_to_string(file_path=file_path_2)
    list_lines_2 = string_2.split('\n')
    list_lines_2.sort()
    
    i_1 = 0
    i_2 = 0
    while i_1 < len(list_lines_1) and i_2 < len(list_lines_2):
        str_1 = list_lines_1[i_1].rstrip()
        str_2 = list_lines_2[i_2].rstrip()
        index_of_end_of_prefix = get_index_of_end_of_shared_prefix(str_1, str_2)
        if index_of_end_of_prefix is None:
            print(f'{formatted_both}: {str_1}')
            i_1 = i_1 + 1
            i_2 = i_2 + 1
        elif '=' in str_1[0:index_of_end_of_prefix] and '=' in str_2[0:index_of_end_of_prefix]:
            # both lines have matching starting variables at least up to the '='

            print(f"{formatted_env_name_1}: {str_1}")
            print(f"{formatted_env_name_2}: {str_2}")
            i_1 = i_1 + 1
            i_2 = i_2 + 1
        elif str_1 < str_2:
            print(f'{formatted_env_name_1}: {str_1}')
            i_1 = i_1 + 1
        elif str_2 > str_1:
            print(f'{formatted_env_name_2}: {str_2}')
            i_2 = i_2 + 1
    
    while i_1 < len(list_lines_1):
        str_1 = list_lines_1[i_1].rstrip()
        print(f"{formatted_env_name_1}: {str_1}")
        i_1 = i_1 + 1
        
            
    while i_2 < len(list_lines_2):
        str_2 = list_lines_2[i_2].rstrip()
        print(f"{formatted_env_name_2}: {str_2}")
        i_2 = i_2 + 1


def main():
    parser = argparse.ArgumentParser(description="Environment Manager")
    
    # Define subparsers for commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # `init` command
    init_parser = subparsers.add_parser("init", help="Initialize the environment")
    init_parser.add_argument("params", nargs="*", help="Parameters for initialization")

    # `load` command
    load_parser = subparsers.add_parser("load", help="Load the environment")
    load_parser.add_argument("params", nargs="*", help="Parameters for loading")

    # `save` command
    save_parser = subparsers.add_parser("save", help="Save the environment")
    # save_parser.add_argument("env_name", nargs="*", help="Name of environment")
    save_parser.add_argument("params", nargs="*", help="Parameters for loading")

    # `list` command
    list_parser = subparsers.add_parser("list", help="list the environment")
    # list_parser.add_argument("env_name", nargs="*", help="Name of environment")
    list_parser.add_argument("params", nargs="*", help="Parameters for loading")
    
    # `clear` command
    clear_parser = subparsers.add_parser("clear", help="clear the environment")
    # clear_parser.add_argument("env_name", nargs="*", help="Name of environment")
    clear_parser.add_argument("params", nargs="*", help="Parameters for loading")
    
    # `delete` command
    delete_parser = subparsers.add_parser("delete", help="delete the environment")
    # delete_parser.add_argument("env_name", nargs="*", help="Name of environment")
    delete_parser.add_argument("params", nargs="*", help="Parameters for loading")
    
    
    # `clearall` command
    clearall_parser = subparsers.add_parser("clearall", help="clearall the environment")
    # clearall_parser.add_argument("env_name", nargs="*", help="Name of environment")
    clearall_parser.add_argument("params", nargs="*", help="Parameters for loading")
    
    # `read` command
    read_parser = subparsers.add_parser("read", help="read the environment")
    # read_parser.add_argument("env_name", nargs="*", help="Name of environment")
    read_parser.add_argument("params", nargs="*", help="Parameters for loading")
    
    # `compare` command
    compare_parser = subparsers.add_parser("compare", help="compare the environment")
    # compare_parser.add_argument("env_name", nargs="*", help="Name of environment")
    compare_parser.add_argument("params", nargs="*", help="Parameters for loading")
    
    args = parser.parse_args()

    # Dispatch command
    if args.command == "init":
        init_env(args.params)
    elif args.command == "load":
        load_env(args.params)
    elif args.command == "save":
        save_env(args.params)
    elif args.command == "list":
        list_envs(args.params)
    elif args.command == "clear":
        clear_env(args.params)
    elif args.command == "delete":
        delete_env(args.params)
    elif args.command == "clearall":
        clearall_env(args.params)
    elif args.command == "read":
        read_env(args.params)
    elif args.command == "compare":
        compare_env(args.params)
        
if __name__ == "__main__":
    if not os.path.exists(path_to_environment_data):
        os.mkdir(path_to_environment_data)
    main()
