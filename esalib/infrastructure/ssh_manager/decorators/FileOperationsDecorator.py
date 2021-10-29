from abc import ABCMeta, abstractmethod
# SSH
from ..SSHConnection import SSHConnection

class FileOperationsDecorator():
    """
    @version 2.3.1

    Especification for the decorator to apply file operations to a SSH strategy.
    It provides the signature for the methods to retrieve or send files (where the retrieve_file 
    method must be implemented mandatorily)
    """
    __metaclass__ = ABCMeta

    # Constructor, it receives a host options object.
    @abstractmethod
    def __init__(
        self, 
        ssh_connection: SSHConnection
    ): raise NotImplementedError

    # Method to retrieve a file, providing the source (the file requesting from remote host), and the destination file (or output file name in local host)
    @abstractmethod
    def retrieve_file(
        self, 
        source_file: str, 
        destination_path: str = None,
    ): raise NotImplementedError

    # Method to upload a file to a remote host
    @abstractmethod
    def send_file(
        self,
        source_file: str,
        destination_path: str
    ): pass



