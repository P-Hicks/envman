from ..abstract_action import AbstractAction
import os
import shutil
from src.actions.action_manager import register_action
from ..abstract_action import AbstractAction
from src.utils.console_utils import confirm_action
from src.utils.file_utils import write_string_to_file
from ..abstract_action import AbstractAction
import os
from src.configs import current_in_use_env_file_path, example_env_file_path
from src.actions.action_manager import register_action
from src.env_parser.env_file_environment_manager import generate_path_to_env

@register_action(
    cmd="save",
    description="save an environment",
)
class SaveAction(AbstractAction):   
    def setup_args(self, arg_parser):
        arg_parser.add_argument("environment_name", help="Environment name")
        return super().setup_args(arg_parser)
    
    def run_action(self, args):
        """Save environment settings."""
        env_name = args.environment_name
        file_path = generate_path_to_env(env_name)
        if not os.path.exists(current_in_use_env_file_path):
            print(f'current envrionment not set. cannot load.')
            exit(0)
        if os.path.exists(file_path ) and not args.no_confirmation:
            confirm_action(f"environment is already set, and will be overridden with current. are you sure?", should_exit_on_no=True)
        shutil.copy(
            dst=file_path,
            src=current_in_use_env_file_path,
        )
        # env = EnvFileEnvironmentManager().parse_environment_from_env_file(env_name, current_in_use_env_file_path)
        # json_str = JsonFileEnvironmentManager().write_json_file_from_environment(path_to_env_file=file_path, env=env)
        
        return super().run_action(args)