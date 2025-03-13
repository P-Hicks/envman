 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINKING = '\033[5m'
    BLACK	= '\033[90m'#	40
    RED	    = '\033[91m'#	41
    GREEN	= '\033[92m'#	42
    YELLOW	= '\033[93m'#	43
    BLUE	= '\033[94m'#	44
    MAGENTA	= '\033[95m'#	45
    CYAN	= '\033[96m'#	46
    WHITE	= '\033[97m'#	47
    DEFAULT	= '\033[99m'#	49
    LEFT_1	= '\033[#D'

def print_w_color(*args, **kwargs):
    color = kwargs.pop('color')
    args = list(args)
    if color is not None:
        args.insert(0, color)
        args.append(bcolors.ENDC)
    print(*args, *kwargs)

def input_w_color(prompt, **kwargs):
    color = kwargs.pop('color')
    if color is not None:
        prompt = color + prompt + bcolors.ENDC 
    return input(prompt, *kwargs)


def confirm_action(prompt : str, should_exit_on_no : bool = False) -> bool:
    confirmation = input_w_color(f'{prompt} (y/n) ', color = bcolors.MAGENTA)
    if confirmation == 'y' or confirmation == 'Y' or confirmation.lower() == 'yes':
        return True
    if should_exit_on_no:
        print('cancelled.')
        exit(1)
    return False