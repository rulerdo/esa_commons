from abc import ABCMeta, abstractmethod
# ESA utils
from ..ESASSHAgent import ESASSHAgent

class Service:
    """
    version 1.0.1
    
    Contract for the services, it specifies the methods that must be implemented, as well as the parameters that they receive.
    """
    __metaclass__ = ABCMeta
    # Path to the service executable
    DEFAULT_SERVICE_PATH = '/data/bin/'

    # Constructor, it receives the ESA SSH angent and the service path
    def __init__(
        self, 
        esa_ssh_agent: ESASSHAgent = None,
        service_path: str = None
    ): 
        self.esa_ssh_agent = esa_ssh_agent
        self.service_path = service_path if service_path != None else self.DEFAULT_SERVICE_PATH

    # Method to set the path to the service executable
    def set_service_path(self, service_path: str):
        self.service_path = service_path

    # Method to set the status of the service
    @abstractmethod
    def set_service_status(
        self,
        service_name: str, 
        service_status: str,
        sleep_time_after_command: float
    ): raise NotImplementedError

    # Method to determine if the service is up and running
    @abstractmethod
    def is_service_active(
        self, 
        service_name: str
    ) -> bool: raise NotImplementedError

    # Method to wait until a service is up and running
    @abstractmethod
    def wait_until_service_is_up(
        self, 
        service_name: str,
        timeout: float,
        sleep_time: float
    ): raise NotImplementedError