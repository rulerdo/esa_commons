# ESA utils
from .ESASSHAgent import ESASSHAgent
from .ESAParameters import LoggerInitializer, ESASSHParameters

class SMAManager:

    def __init__(self):
        # We initialize the logger
        # We don't retrieve the SSHParameters from ESAParameters, because they define the parameters for the ESA, not the SMA.
        LoggerInitializer.initialize()
        # To be defined later
        self.ssh_agent: ESASSHAgent = None
        self.ssh_parameters: ESASSHParameters = None 

    def initialize(self):
        """Facade to retrieve the SSH parameters and start the connection."""
        self.set_ssh_parameters()
        self.start_connection()

    def set_ssh_parameters(self):
        """Retrieves the parameters for the SSH connection to SMA."""
        sma_ip = input('Enter the SMA IP address or domain: ')
        sma_user = input('Enter the SSH user: ')
        sma_password = input('Enter the SSH password: ')
        # We set the custom SSH port if provided
        sma_ssh_port_custom = input('Enter the SMA SSH port [22]: ')
        sma_ssh_port = sma_ssh_port_custom if sma_ssh_port_custom else 22
        # We create the SSHParameters object
        self.ssh_parameters = ESASSHParameters(
            esa_ip = sma_ip,
            esa_user = sma_user,
            esa_password = sma_password,
            esa_ssh_port = sma_ssh_port
        )

    def start_connection(self):
        """Starts the SSH connection to SMA."""
        self.ssh_agent = ESASSHAgent(self.ssh_parameters)
        self.ssh_agent.start_connection()

    def close_connection(self):
        """Closes the SSH connection to SMA."""
        self.ssh_agent.close_connection()

    def get_ssh_agent(self) -> ESASSHAgent:
        """Returns the SSH agent."""
        return self.ssh_agent
    


