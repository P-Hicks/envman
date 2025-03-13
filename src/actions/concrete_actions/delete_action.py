from ..abstract_action import AbstractAction
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
    cmd="delete",
    description="delete a saved environment",
)
class DeleteAction(AbstractAction):   
    def setup_args(self, arg_parser):
        arg_parser.add_argument("environment_name", help="Environment name")
        return super().setup_args(arg_parser)
    
    def run_action(self, args):
        env_name = args.environment_name
        file_path = generate_path_to_env(env_name=env_name)
        if not os.path.exists(file_path):
            print(f'envrionment {env_name} not set. cannot delete.')
            exit(0)
        if os.path.exists(file_path ) and not args.no_confirmation:
            confirm_action(f"environment is set, are you sure you want to delete?", should_exit_on_no=True)
        os.remove(
            path=file_path
        )
        return super().run_action(args)