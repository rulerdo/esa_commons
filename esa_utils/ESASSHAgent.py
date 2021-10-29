import time
# SSH
from esa_utils.ESAParameters import ESASSHParameters
from infrastructure.ssh_manager.SSHManager import SSHManager
# SCP file transfer
from infrastructure.ssh_manager.SCPFileTransfer import SCPFileTransfer
# Utils
from utils.logger.Logger import Logger


class ESASSHAgent:
    """
    @version 3.6.0

    SSH agent for the ESA. It provides a predictable mechanism to initialize and keep a SSH connection.
    File transfer functionalities via SCP are also available.
    """
    def __init__(
        self,
        ssh_parameters: ESASSHParameters
    ):
        """
        @param {str} esa_ip IP of the ESA.
        @param {str} esa_user SSH user of the ESA.
        @param {str} esa_password SSH password for the ESA user.
        @param {int} esa_ssh_port Port where the SSH service is running on ESA.
        """
        self.esa_ip = ssh_parameters.esa_ip
        self.esa_user = ssh_parameters.esa_user
        self.esa_password = ssh_parameters.esa_password
        self.esa_ssh_port = ssh_parameters.esa_ssh_port

    def start_connection(self):
        """
        Initializes the SSHManager and sets the connection to the local state.
        """
        SSHManager.initialize({  
            'hostname': self.esa_ip, 
            'username': self.esa_user, 
            'password': self.esa_password, 
            'port': self.esa_ssh_port, 
        })
        Logger.info('Connected via SSH')

        # We copy the reference to the session to a member variable
        self.ssh_connection = SSHManager.get_connection()

    def get_ssh_connection(self):
        """
        @returns The SSH connection instance.

        Getter method for the SSH connection.
        """
        return self.ssh_connection

    def execute_command(self, command: str) -> str: 
        """
        @param {str} command Command to execute.

        Executes a command and keeps the outpout in the SSHManager buffer, which is also returned.
        """
        return SSHManager.exec_command(command, return_output = True, clear_buffer_before = True)

    def execute_cli_command(
        self, 
        command: str,
        timeout: float = 5,
        sleep_time: float = 0.1,
        buffer_size: int = 4096
    ) -> str:
        """
        @param {str} command Command to execute.
        @param {float} timeout The time to wait before raising a timeout exception while expecting a command output (5s by default).
        @param {float} sleep_time The time to wait between output lectures (0.1s or 100ms by default).
        @param {int} buffer_size The size of the buffer where the async aoutput is going to be stored (4096 bytes by default).

        Executes a command in CLI mode and keeps the outpout in the SSHManager buffer, which is also returned.
        """
        # We set the channel properties
        SSHManager.set_channel_properties(timeout, sleep_time, buffer_size)
        # Enters to the CLI mode
        SSHManager.exec_async_command('csh', terminal_delimiter = ']')
        SSHManager.exec_async_command('cli', terminal_delimiter = '(SERVICE)>')
        # Executes the command at CLI level
        output = SSHManager.exec_async_command(command, terminal_delimiter = '(SERVICE)>')
        # Exits the CLI mode
        SSHManager.exec_async_command('exit', terminal_delimiter = ']')
        SSHManager.exec_async_command('exit', terminal_delimiter = '#', close_channel_after = True)
        return output


    def clear_output_buffer(self):
        """
        Clears the SSHManager output buffer (the one that stores the output from commands).
        """
        SSHManager.clear_buffer()

    def get_command_output(self) -> str:
        """
        Returns the SSHManager output buffer, with the outputs from commands.
        """
        return SSHManager.get_output()


    def get_file_with_scp(self, path_to_file: str):
        """
        @param {str} path_to_file Path of the remote file to retrieve.

        Retrieves a file from the ESA via the SCPFileTransfer wrapper.
        """
        SCPFileTransfer(self.ssh_connection).get_file(path_to_file)

    def upload_file_with_scp(
        self, 
        file_to_upload: str,
        destination_path: str
    ):
        """
        @param {str} file_to_upload Path to the local file to upload.
        @param {str} destination_path Remote path where the uploaded file will be installed.

        Uploads a file to the ESA, using SCPFileTransfer wrapper.
        """
        SCPFileTransfer(self.ssh_connection).upload_file(file_to_upload, destination_path)
    


