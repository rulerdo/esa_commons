from paramiko import SSHClient, AutoAddPolicy
from paramiko.channel import Channel
# SSH
from infrastructure.ssh_manager.strategy.SSHStrategy import SSHStrategy
# Utils
from utils.validators.IteratorValidator import IteratorValidator

class ParamikoStrategy(SSHStrategy):
    """
    @version 2.2.1
    
    SSH strategy, implementing paramiko library for multi-vendor support.
    It receives an options list with the following shape:

    host = {
        'hostname': '10.10.10.10', 
        'username': 'user', 
        'password': 'password',
        'port': 22
    }
    """

    def __init__(self, options):
        self.options = options
        self.channel: Channel = None
    
    def connect(self):
        """
        Connect method specific for the paramiko library.
        """
        self.connection = SSHClient()
        self.connection.set_missing_host_key_policy(AutoAddPolicy())
        self.connection.connect(**self.options)
        return self.connection.get_transport()

    def get_connection(self):
        """
        Method to get the connection instance
        """
        return self.connection.get_transport()

    def disconnect(self):
        """
        Disconnect method specific for the paramiko library.
        """
        return self.connection.close()
    
    def execute_command(self, command: str) -> str:
        """
        @param {str} command The command to execute.

        Execute command, specific for the paramiko library.
        """
        _, stdout, __ = self.connection.exec_command(command)
        # We return the decoded output from stdout
        return stdout.read().decode()

    def execute_async_command(
        self, 
        command: str,
        terminal_delimiter: str,
        close_channel_after: bool,
    ):
        """
        @param {str} command The command to execute.
        @param {str} terminal_delimiter The characters sequence that comes before the cursor at the terminal (like ~$ in Linux).
        @param {bool} close_channel_after Flag to indicate if the channel should be closed after the command execution.

        Executes commands whose output could be delayed or by steps, specific for the paramiko library. We  make use of the 
        async_command_output helper, to wait for the whole output based on the terminal delimiter sequence (like ~$ in Linux).
        """
        # We open a new a channel, to get more control over the command output reception
        if not self.channel or not self.channel.active:
            self.channel = self.connection.invoke_shell()
        # We execute the command, and wait until it is complete to get the output
        self.channel.send(f'{ command }\n')
        output = self.__get_async_command_output(terminal_delimiter)
        # We close the channel and return the output
        if close_channel_after:
            self.channel.close()
        return output


    def set_channel_properties(
        self, 
        timeout: float, 
        sleep_time: float, 
        buffer_size: int
    ) -> None:
        """
        @param {float} timeout The maximum number of seconds to wait before resolution.
        @param {float} sleep_time The number of seconds to wait before reading the buffer again, when waiting for an output.
        @param {int} buffer_size The number of bytes to read from the channel output.
        """
        self.timeout = timeout
        self.sleep_time = sleep_time
        self.buffer_size = buffer_size
        

    # Internal helpers

    def __get_async_command_output(self, terminal_delimiter: str) -> str:
        """
        @param {str} terminal_delimiter The characters sequence that comes before the cursor at the terminal (like ~$ in Linux).

        Waits for the output of an async or delayed output command, we receive data until we find the terminal delimiter.
        We wait for $sleep_time seconds on every iteration and we stop the process if $timeout is reached, which is validated with
        the IteratorValidator timeout generator util.
        """
        if not self.channel or not self.channel.active:
            raise Exception('Channel is not open')
        # We initialize the response and the iterator validator (which is a generator function, so it must be initialized)
        response = ''
        iterations_validator = IteratorValidator.iterator_with_timeout(self.timeout, self.sleep_time)
        # We receive data from the channel until we find the terminal delimiter (The characters before the stdin cursor)
        while response.find(terminal_delimiter) == -1:
            response += self.channel.recv(self.buffer_size).decode()
            # We update the iterations and validate the constraint via the generator
            next(iterations_validator)
        return response