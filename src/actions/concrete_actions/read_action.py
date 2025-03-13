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


@register_action(
    cmd="read",
    description="read a saved environment to the terminal",
)
class ReadAction(AbstractAction):   
    def setup_args(self, arg_parser):
        arg_parser.add_argument("environment_name", help="Environment name")
        return super().setup_args(arg_parser)
    
    def run_action(self, args):
        env_name = args.environment_name
        file_path = generate_path_to_env(env_name=env_name)
        if not os.path.exists(file_path):
            print(f'Error: environment {env_name} does not exist.')
            exit(1)
        string = read_file_to_string(file_path=file_path)
        print(string)
        return super().run_action(args)