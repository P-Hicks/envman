from src.cmd_parser.cmd_parser import default_addition_of_args

class ActionItem():
    def __init__(self, cmd="", description="", action=None):
        self.cmd = cmd
        self.description = description
        self.action = action

class ActionManager():
    def __init__(self):
        self.actions = []
        
    def add_action(self, action):
        self.actions.append(action)

default_action_manager = ActionManager()

def register_action(cmd:str = "", description : str = ""):
    
    def inner_dec(action_class):
        
        default_action_manager.add_action(
            ActionItem(
                cmd=cmd,
                description=description,
                action=action_class(),
            )
        )
        
        return action_class
    
    return inner_dec

def setup_actions_as_subcommands(subparser):
    for action in default_action_manager.actions:
        action_parser = subparser.add_parser(action.cmd, help=action.description, )
        default_addition_of_args(action_parser)
        action.action.setup_args(action_parser)
        

def perform_command(args):
    cmd = args.command
    for action in default_action_manager.actions:
        if action.cmd == cmd:
            action.action.run_action(args)
        return