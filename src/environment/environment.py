
class EnvironmentVariable:
    def __init__(self, key = None, value = None, comment = None):
        self._key = key
        self._value = value
        self._comment = comment

class Environment:
    def __init__(self, name):
        self._name = name
        self._variables : list[EnvironmentVariable] = []

    def add_variable(self, var : EnvironmentVariable):
        self._variables.append(var)
       
    