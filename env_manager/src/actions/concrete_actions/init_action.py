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

@register_action(
    cmd="init",
    description="initialize the current working environment (with a default environment)",
)
class InitAction(AbstractAction):   
    def setup_args(self, arg_parser):
        return super().setup_args(arg_parser)
    
    def run_action(self, args):
        """Initialize the environment with given arguments."""
        if os.path.exists(current_in_use_env_file_path) and not args.no_confirmation:
            confirm_action(f"environment is already set, and will be overridden with default. are you sure?", should_exit_on_no=True)
        shutil.copy(
            src=example_env_file_path,
            dst=current_in_use_env_file_path,
        )