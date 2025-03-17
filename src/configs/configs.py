
import json
import os
from src.utils.file_utils import read_file_to_string, write_string_to_file


is_case_sensitive = False
should_prompt = True
current_in_use_env_file_path = ".env"
example_env_file_path = "example.env"

# envrionment settings - do not make configurable
path_to_environment_data = '.envman'
path_to_config_file = f'{path_to_environment_data}/config.json'

def read_json_file(path):
    contents = read_file_to_string(path)
    data = json.loads(contents)
    return data

def get_configs():
    if not os.path.exists(path_to_environment_data):
        os.mkdir(path_to_environment_data)
    if not os.path.exists(path_to_config_file):
        write_string_to_file(path_to_config_file, content='{}')
    configs = read_json_file(path_to_config_file)
    
    return configs 
    
    
def parse_configs():
    configs = get_configs()
    
    if configs.get('is_case_sensitive') is not None:
        global is_case_sensitive
        is_case_sensitive = configs['is_case_sensitive'] 
    if configs.get('should_prompt') is not None:
        global should_prompt
        should_prompt = configs['should_prompt'] 
    if configs.get('current_in_use_env_file_path') is not None:
        global current_in_use_env_file_pat
        current_in_use_env_file_pat = configs['current_in_use_env_file_pat']
    if configs.get('example_env_file_path') is not None:
        global example_env_file_path
        example_env_file_path = configs['example_env_file_path'] 
    
    
    
    
    
    
    