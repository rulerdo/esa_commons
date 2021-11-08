from abc import ABCMeta, abstractmethod

class SSHStrategy:
    """
    version 3.4.1
    
    Contract for the SSH strategies, it specifies the methods that must be implemented, as well as the parameters that they receive.
    """
    __metaclass__ = ABCMeta

    # Constructor, it receives a host options object.
    @abstractmethod
    def __init__(
        self, 
        options
    ): raise NotImplementedError

    # Connection entry point, any required methods by strategy must be invoked here.
    @abstractmethod
    def connect(self): raise NotImplementedError

    # Connection getter.
    @abstractmethod
    def get_connection(self): raise NotImplementedError

    # Disconnection entry point, any required methods by strategy must be invoked here.
    @abstractmethod
    def disconnect(self): raise NotImplementedError

    # Method to execute commands. It must return the output of the command.
    @abstractmethod
    def execute_command(self, command: str) -> str: raise NotImplementedError

    # Method to execute commands whose output could be delayed. It must return the output of the command.
    @abstractmethod
    def execute_async_command(
        self, 
        command: str,
        terminal_delimiter: str,
        close_channel_after: bool,
        more_output_delimiter: str,
    ) -> str: pass

    # Method to set the channel properties (for execute_async_command and other methods)
    @abstractmethod
    def set_channel_properties(
        self,
        timeout: float,
        sleep_time: float,
        buffer_size: int
    ) -> None: pass



