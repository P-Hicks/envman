
def none_are_null(*args):
    for arg in args:
        if arg is None:
            return False
    return True