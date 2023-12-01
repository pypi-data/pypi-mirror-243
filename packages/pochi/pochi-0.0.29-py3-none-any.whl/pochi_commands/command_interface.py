from abc import ABC, abstractmethod


class CommandInterface(ABC):
    @abstractmethod
    def __init__(self, parser):
        pass

    @abstractmethod
    def get_help_text(self):
        pass

    @abstractmethod
    def execute(self, options):
        pass
