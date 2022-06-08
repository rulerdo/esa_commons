# Tunnels utils
from .ESASSHAgent import ESASSHAgent
from .ESAParameters import LoggerInitializer, ESASSHParameters

import argparse
import os
from collections import namedtuple

class TunnelsManager:

    def __init__(self):
        # We initialize the logger
        # We don't retrieve the SSHParameters from ESAParameters, because they define the parameters for the Tunnels.
        LoggerInitializer.initialize()
        # To be defined later
        self.ssh_agent: ESASSHAgent = None
        self.ssh_parameters: ESASSHParameters = None
        self.tunnels_parmeters: TunnelsCLIArguments = None

    def initialize(self):
        """Facade to retrieve the SSH parameters and start the connection."""
        self.set_ssh_parameters()
        self.set_esa_credentials()
        self.start_connection()

    def set_ssh_parameters(self):
        # We create the SSHParameters object
        tunnels_ip = self.tunnels_parmeters.params.tunnels_host
        tunnels_user = self.tunnels_parmeters.params.user
        tunnels_password = self.tunnels_parmeters.params.password

        self.ssh_parameters = ESASSHParameters(
            esa_ip = tunnels_ip,
            esa_user = tunnels_user,
            esa_password = tunnels_password,
            esa_ssh_port = 22
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
        serial_number = self.tunnels_parmeters.params.serial_number
        seed = self.tunnels_parmeters.params.seed

        self.credentials = (serial_number, seed)
        self.command_prefix = f'tunnels -L {serial_number} -p {seed}'

    def get_file_tunnels(self,file,path):
        abs_filename = path + file

        print(f'Downloading {file} from ESA...')
        output = self.ssh_agent.execute_command(f'echo { self.command_prefix } -G {abs_filename}')
        print(output)

        print(f'Copying {file} to local host')
        self.ssh_agent.get_file_with_scp(file)
        print('File copied from ESA -> Tunnels and from Tunnels --> Host')


    def put_file_tunnels(self,file,path):
        abs_filename = path + file

        print(f'Uploading {file} to Tunnels...')
        self.ssh_agent.upload_file_with_scp(file, '.')
        print(f'{file} uploaded!')

        print(f'Uploading {file} to ESA...')
        output = self.ssh_agent.execute_command(f'echo { self.command_prefix } -P {abs_filename}')
        print(output)
        print(f'{file} uploaded to /tmp on ESA')

        print(f'Connecting to ESA terminal...')
        output = self.ssh_agent.execute_command(f'echo { self.command_prefix } -C')
        print(output)

        print(f'Moving {file} to final location...')
        output = self.ssh_agent.execute_command(f'echo "mv /tmp/{file} {abs_filename}"')
        print(output)

    def cleanup_temp_file_tunnels(self,file,local=False):
        print(f'Cleaning up {file} temp copies')

        # Delete file on Tunnels server
        output = self.ssh_agent.execute_command(f'echo "rm {file}"')
        print(output)

        # Delete local file
        if local:
            os.remove(file)

        print(f'{file} deleted from tunnels and local host')

class TunnelsCLIArguments(argparse.ArgumentParser):

    def __init__(self):
        super().__init__()
        self.__add_tunnel_arguments()
        self.params = self.__get_tunnels_arguments()

    def __add_tunnel_arguments(self):
        self.add_argument('-t', '--tunnels-host', help = 'IP or hostname of Tunnel Server')
        self.add_argument('-u', '--user', help = 'User on server')
        self.add_argument('-p', '--password', help = 'Password on server')
        self.add_argument('-n', '--serial-number', help = 'Serial number of the ESA')
        self.add_argument('-s', '--seed', help = 'Seed used to connect to the ESA')

    def __get_tunnels_arguments(self):
        args = self.__add_tunnel_arguments().arguments

        Tunnels = namedtuple('Tunnel parameters', 'tunnels_host user password serial_number seed')

        self.params = Tunnels(args.tunnels_host, args.user, args.password, args.serial_number, args.seed)

        return self.params