# Tunnels utils
from .ESASSHAgent import ESASSHAgent
from .ESAParameters import LoggerInitializer, ESASSHParameters

class TunnelsManager:

    def __init__(self):
        # We initialize the logger
        # We don't retrieve the SSHParameters from ESAParameters, because they define the parameters for the Tunnels.
        LoggerInitializer.initialize()
        # To be defined later
        self.ssh_agent: ESASSHAgent = None
        self.ssh_parameters: ESASSHParameters = None

    def initialize(self):
        """Facade to retrieve the SSH parameters and start the connection."""
        self.set_ssh_parameters()
        self.start_connection()

    def set_ssh_parameters(self):
        """Retrieves the parameters for the SSH connection to the Tunnels."""
        tunnels_ip = input('Enter the Tunnels IP address or domain: ')
        tunnels_user = input('Enter the SSH user: ')
        tunnels_password = input('Enter the SSH password: ')
        # We set the custom SSH port if provided
        tunnels_ssh_port_custom = input('Enter the Tunnels SSH port [22]: ')
        tunnels_ssh_port = tunnels_ssh_port_custom if tunnels_ssh_port_custom else 22
        # We create the SSHParameters object
        self.ssh_parameters = ESASSHParameters(
            esa_ip = tunnels_ip,
            esa_user = tunnels_user,
            esa_password = tunnels_password,
            esa_ssh_port = tunnels_ssh_port
        )

    def start_connection(self):
        """Starts the SSH connection to Tunnels."""
        self.ssh_agent = ESASSHAgent(self.ssh_parameters)
        self.ssh_agent.start_connection()

    def close_connection(self):
        """Closes the SSH connection to Tunnels."""
        self.ssh_agent.close_connection()

    def get_ssh_agent(self) -> ESASSHAgent:
        """Returns the SSH agent."""
        return self.ssh_agent



