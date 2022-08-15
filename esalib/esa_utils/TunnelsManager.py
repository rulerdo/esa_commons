# Tunnels utils
from .ESASSHAgent import ESASSHAgent
from .ESAParameters import LoggerInitializer, ESASSHParameters
import yaml

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
        self.set_esa_credentials()
        self.start_connection()

    def set_ssh_parameters(self):
        """Retrieves the parameters for the SSH connection to the Tunnels."""

        with open('config.yaml', 'r') as f:
            variables = yaml.safe_load(f)

        tunnels_ip = variables['TUNNELS_SERVER']
        tunnels_user = variables['TUNNELS_USER']
        tunnels_password = variables['TUNNELS_PASSWORD']
        # We set the custom SSH port if provided
        tunnels_ssh_port = variables['TUNNELS_PORTD']
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

    def set_esa_credentials(self):

        with open('config.yaml', 'r') as f:
            variables = yaml.safe_load(f)

        serial_number = variables['ESA_SERIAL']
        seed_id = variables['ESA_SEED']
        self.credentials = (serial_number, seed_id)
        self.command_prefix = f'tunnels -L {serial_number} -p {seed_id}'