# SSH
from .SSHConnection import SSHConnection
from .strategy.ParamikoStrategy import ParamikoStrategy
# Strategy contract
from .strategy.SSHStrategy import SSHStrategy

class SSHManager:
    """
    @version 3.4.1
    
    Class to establish an SSH connection with a device implementing the Singleton pattern, to keep a single 
    instance of the connection through all the process. 
    It is also a container for the different strategies, to support various implementations or libraries. 
    Finally, it also provides a functionality to keep the output of the entered commands in a buffer, 
    which can also be cleared or retrieved on demand.
    """
    # Strategy static parameter
    __strategy = None
    # Reference to SSH connection
    __connection = None

    @staticmethod
    def initialize(
        strategy: SSHStrategy
    ): 
        """
        @param {SSHStrategy} strategy Startegy to use as SSH implementation.

        Method to set the instance in a Singleton-compliant way, so that this can be invoked anywhere and,
        ideally, only once.
        """
        SSHManager.buffer = ''
        SSHManager.__strategy = strategy
        # We set the connection for the provided strategy
        SSHManager.__set_connection()

    @staticmethod
    def initialize(
        host_options
    ):
        """
        @param {dict} host_options The options to start the connection with the remote host.

        Method to set the instance in a Singleton-compliant way, so that this can be invoked anywhere and,
        ideally, only once. It is an alternate way of initializing the SSH manager without a concrete strategy
        it defaults to the Paramiko, so it only receives the host options for that strategy.
        """
        SSHManager.buffer = ''
        SSHManager.__strategy = ParamikoStrategy(host_options)
        # We set the connection for the provided strategy
        SSHManager.__set_connection() 

    @staticmethod
    def set_strategy(strategy: SSHStrategy):
        """
        @param {SSHStrategy} strategy Concrete implementation of SSH (strategy) to apply.
        
        Method to set the SSH strategy to apply (basically related to the library in use)
        """
        SSHManager.__strategy = strategy
        # We set the connection once again, using the new strategy
        SSHManager.__set_connection()

    @staticmethod
    def get_strategy() -> SSHStrategy:
        """
        Method to get the current SSH strategy that is being applied

        @returns {SSHStrategy}
        """
        return SSHManager.__strategy

    @staticmethod
    def __connect():
        """
        Method to start the connection.

        @returns {object} SSH connection.
        """
        return SSHManager.__strategy.connect()

    @staticmethod
    def disconnect():
        """
        Method to close the connection.
        """
        SSHManager.__strategy.disconnect()
        SSHConnection.set_connection(None)

    @staticmethod
    def __set_connection():
        """
        Method to set the connection instance
        """
        # We set the connection instance in the Singleton container (SSHConnection)
        SSHConnection.set_connection(
            SSHManager.__connect() if SSHManager.__strategy else None
        )
        # We set the connection reference locally
        SSHManager.__connection = SSHConnection.get_connection()

    @staticmethod
    def get_connection():
        """
        Method to get the connection instance reference.

        @returns {object} SSH connection.
        """
        return SSHManager.__connection
    
    @staticmethod
    def exec_command(
        command: str, 
        return_output: bool = True,
        clear_buffer_before: bool = True
    ):
        """
        @param {str} command The command to execute.
        @param {bool} return_output Flag to indicate that the output of the command is returned (enabled by default).
        @param {bool} clear_buffer_befor Flag to indicate that the output buffer should be cleared before the execution 
        of that command, to get the output relative to that command only (enabled by default).
        
        Method to execute a command. It writes the result to the buffer.
        """
        # We validate the startegy existance before executing the command
        if not SSHManager.__strategy:
            raise Exception('Strategy must be specified.')
        # We clear the output buffer (unless it is disabled)
        if clear_buffer_before: SSHManager.clear_buffer()
        # We execute the command and store the output
        SSHManager.buffer += SSHManager.__strategy.execute_command(command)
        # We return the output unless it was not indicated
        if return_output: return SSHManager.buffer

    @staticmethod
    def exec_async_command(
        command: str, 
        terminal_delimiter: str = '~$',
        close_channel_after: bool = False,
    ):
        """
        @param {str} command The command to execute.
        @param {str} terminal_delimiter The characters sequence that comes before the cursor at the terminal (like ~$ in Linux).
        @param {bool} close_channel_after Flag to indicate if the channel should be closed after the command execution.

        Method to execute an async command (a command whose output may be delayed).
        """
        # We validate the startegy existance before executing the command
        if not SSHManager.__strategy:
            raise Exception('Strategy must be specified.')
        # We execute the command and return the output
        return SSHManager.__strategy.execute_async_command(
            command,
            terminal_delimiter,
            close_channel_after
        )

    @staticmethod
    def set_channel_properties(
        timeout: float,
        sleep_time: float,
        buffer_size: int
    ):
        """
        @param {float} timeout The maximum number of seconds to wait before resolution.
        @param {float} sleep_time The number of seconds to wait before reading the buffer again, when waiting for an output.
        @param {int} buffer_size The number of bytes to read from the channel output.

        Sets the channel properties at strategy level.
        """
        # We validate the startegy existance before executing the command
        if not SSHManager.__strategy:
            raise Exception('Strategy must be specified.')
        # We set the properties at channel level
        SSHManager.__strategy.set_channel_properties(
            timeout,
            sleep_time,
            buffer_size
        )


    @staticmethod
    def get_output() -> str:
        """
        Method to print the return the output buffer.

        @returns {str} The output buffer.
        """
        return SSHManager.buffer

    @staticmethod
    def clear_buffer():
        """
        Method to clear the output buffer
        """
        SSHManager.buffer = ''
