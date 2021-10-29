from scp import SCPClient
# File operations contract
from ..decorators.FileOperationsDecorator import FileOperationsDecorator


class WithSCPDecorator(FileOperationsDecorator):
    """
    @version 3.5.3

    SSH strategy, implementing netmiko library for multi-vendor support with SCP functionality (via a decorator).
    It receives an options list with the following shape:

    """

    def __init__(self, ssh_connection):
        """
        @param {SSHConnection} ssh_connection The reference to the SSH connection, it is used as the transport for SCPClient.
        """
        self.ssh_connection = ssh_connection

    def retrieve_file(
        self, 
        source_file, 
    ) -> dict[str, bool]:
        """
        @param {str} source_file  The remote path, the path where the remote file is located

        Facade method to retrieve the file from a remote host, it starts the SCP connection and retrieves the 
        files by calling the respective methods with the appropiate options.
        """
        scp_client = SCPClient(self.ssh_connection)
        scp_client.get(source_file)
        scp_client.close()

    def send_file(
        self, 
        source_file: str, 
        destination_path: str
    ):
        """
        @param {str} source_file The local path of the file to send to the rempote host.
        @param {str} destination_file The remote path, the path where the uploaded file will be installed.

        Facade method to upload a file from a remote host, it starts the SCP connection and transfer the files 
        by calling the respective methods with the appropiate options.
        """
        scp_client = SCPClient(self.ssh_connection)
        scp_client.put(source_file, destination_path)
        scp_client.close()







