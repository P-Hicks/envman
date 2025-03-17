from src.utils.console_utils import confirm_action
from src.utils.file_utils import write_string_to_file
from ..abstract_action import AbstractAction
import os
from src.configs.configs import current_in_use_env_file_path
from src.actions.action_manager import register_action

@register_action(
    cmd="clear",
    description="clear the current working environment",
)
class ClearAction(AbstractAction):   
    def setup_args(self, arg_parser):
        return super().setup_args(arg_parser)
    
    def run_action(self, args):
        if os.path.exists(current_in_use_env_file_path ) and not args.no_confirmation:
            confirm_action(f"current environment is set, and will be deleted. are you sure?", should_exit_on_no=True)
        write_string_to_file(
            file_path=current_in_use_env_file_path,
            content=''
        )