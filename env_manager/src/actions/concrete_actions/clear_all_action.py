from src.utils.console_utils import confirm_action
from src.utils.file_utils import write_string_to_file
from ..abstract_action import AbstractAction
import os
from src.configs import current_in_use_env_file_path, path_to_environment_data
from src.actions.action_manager import register_action

@register_action(
    cmd="clearall",
    description="clear all saved environments",
)
class ClearAllAction(AbstractAction):   
    def setup_args(self, arg_parser):
        return super().setup_args(arg_parser)
    
    def run_action(self, args):
        envs = os.listdir(path_to_environment_data)
        env_file_ending = '.env'
        if not args.no_confirmation:
            confirm_action(f"are you sure you want to delete ALL saved environments?", should_exit_on_no=True)
        envs = [
            env for env in envs if env.endswith(env_file_ending)
        ]
        print(f'{len(envs)} development environments found...')
        for env in envs:
            print(f'removing {env}...')
            os.remove(f'{path_to_environment_data}/{env}')    