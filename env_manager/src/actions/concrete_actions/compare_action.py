from ..abstract_action import AbstractAction
from ..abstract_action import AbstractAction
from ..abstract_action import AbstractAction
import os
import shutil
from src.actions.action_manager import register_action
from ..abstract_action import AbstractAction
from src.utils.console_utils import confirm_action
from src.utils.file_utils import write_string_to_file, read_file_to_string
from ..abstract_action import AbstractAction
import os
from src.configs import current_in_use_env_file_path, example_env_file_path
from src.actions.action_manager import register_action
from src.env_parser.env_file_environment_manager import generate_path_to_env


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



@register_action(
    cmd="compare",
    description="compare two saved environments",
)
class CompareAction(AbstractAction):   
    def setup_args(self, arg_parser):
        arg_parser.add_argument("environment_1_name", help="1st Environment name")
        arg_parser.add_argument("environment_2_name", help="2nd Environment name")
        return super().setup_args(arg_parser)
    
    def run_action(self, args):
        env_name_1 = args.environment_1_name
        env_name_2 = args.environment_2_name
        
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
        return super().run_action(args)