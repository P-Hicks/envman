from abc import ABC, abstractmethod
import argparse

class AbstractAction(ABC):
    @abstractmethod
    def setup_args(self, arg_parser : argparse.ArgumentParser):
        pass
    
    @abstractmethod
    def run_action(self, args):
        pass