# SCP decorator
from infrastructure.ssh_manager.decorators.WithSCPDecorator import WithSCPDecorator


class SCPFileTransfer:
    """
    @version 2.5.3
    
    Wrapper for the SCP decorator for SSH transport. It simplifies the usage of this functionality by 
    encapsulating the decoration of the SSH connection.
    """
    def __init__(
        self,
        ssh_connection
    ):
        """
        @param ssh_connection The SSH connection instance.
        """
        self.ssh_connection = ssh_connection
        # We decorate the strategy with file transfer functionality with SCP
        self.ssh_manager_with_scp = WithSCPDecorator(self.ssh_connection)

    def get_file(
        self,
        source_file
    ):
        """
        @param {str} source_file Path to the source file, including it's name and extension

        Method that applies the WithSCPDecorator to the SSH connection to retrieve a file.
        """
        # We get the file
        self.ssh_manager_with_scp.retrieve_file(source_file)

    def upload_file(
        self,
        file_to_upload: str,
        destination_path: str
    ):
        """
        @param {str} file_to_upload Path to the local file, where the file to upload is located, including it's name and extension
        @param {str} destination_path Remote path where the uploaded file will be installed.

        Method that applies the WithSCPDecorator to the SSH connection to send a file.
        """
        self.ssh_manager_with_scp.send_file(file_to_upload, destination_path)


