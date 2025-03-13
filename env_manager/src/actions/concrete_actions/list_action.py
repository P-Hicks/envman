from ..abstract_action import AbstractAction
import os
import shutil
from src.actions.action_manager import register_action
from ..abstract_action import AbstractAction
from src.utils.console_utils import confirm_action
from src.utils.file_utils import write_string_to_file
from ..abstract_action import AbstractAction
import os
from src.configs import current_in_use_env_file_path, example_env_file_path, path_to_environment_data
from src.actions.action_manager import register_action
from src.env_parser.env_file_environment_manager import generate_path_to_env


@register_action(
    cmd="list",
    description="list environments available to load",
)
class ListAction(AbstractAction):   
    def setup_args(self, arg_parser):
        return super().setup_args(arg_parser)
    
    def run_action(self, args):
        envs = os.listdir(path_to_environment_data)
        env_file_ending = '.env'
        envs = [
            env for env in envs if env.endswith(env_file_ending)
        ]
        print(f'{len(envs)} development environments found...')
        for env in envs:
            env_name = env[0:-len(env_file_ending)]
            print(env_name)
        return super().run_action(args)