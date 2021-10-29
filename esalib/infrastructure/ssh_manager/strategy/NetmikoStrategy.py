from netmiko import ConnectHandler
# SSH
from .SSHStrategy import SSHStrategy

class NetmikoStrategy(SSHStrategy):
    """
    @version 2.1.0

    SSH strategy, implementing netmiko library for multi-vendor support.
    It receives an options list with the following shape:

    host = {
        'device_type': 'cisco_ios',
        'host':   '10.10.10.10',
        'username': 'user',
        'password': 'password',
        'port' : 22, # optional, defaults to 22
        'secret': 'cisco', # optional, defaults to ''
    }
    """
    
    def __init__(self, options):
        self.options = options
    
    def connect(self):
        """
        Connect method specific for the netmiko library.
        """
        self.connection = ConnectHandler(
            **self.options
        )
        return self.connection

    def get_connection(self):
        """
        Method to get the connection instance
        """
        return self.connection

    def disconnect(self):
        """
        Disconnect method specific for the netmiko library.
        """
        return self.connection.disconnect()
    
    def execute_command(self, command: str) -> str:
        """
        Execute command, specific for the netmiko library.
        """
        return self.connection.send_command(command)