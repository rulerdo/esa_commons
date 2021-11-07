import argparse    
from dataclasses import dataclass
# Utils
from ..utils.logger.Logger import Logger
from ..utils.files.FileManager import FileManager


@dataclass
class ESASSHParameters:
    """Class to encapsulate ESA SSH parameters."""
    esa_ip: str
    esa_user: str
    esa_password: str
    esa_ssh_port: int = 22


@dataclass 
class ESAEmailParameters:
    """Class to encapsulate ESA email parameters."""
    send_case_email: bool
    case_owner_email: str
    case_identification_number: str


class ESACLIArguments(argparse.ArgumentParser):
    """
    @version 1.0.0

    Class to register and manage the CLI arguments.
    """
    def __init__(self):
        """Initializes the parser."""
        super().__init__()
        self.initialize()

    def initialize(self):
        """Method to add all the CLI arguments"""
        self.__add_log_arguments()
        self.__add_ssh_arguments()
        self.__add_email_arguments()
        self.arguments = self.parse_args() 

    def __add_log_arguments(self):
        """Method to register the logging CLI arguments"""
        self.add_argument('--verbose', dest='verbose', action='store_true')
        self.set_defaults(verbose = False)
        self.add_argument('-l', '--logfile-name', help = 'Local logfile name', default = 'app.log')

    def __add_ssh_arguments(self):
        """Method to register the CLI SSH arguments"""
        self.add_argument('-i', '--esa-ip', help = 'ESA IP', default = '0.0.0.0')
        self.add_argument('-u', '--esa-user', help = 'ESA SSH user', default = 'service')
        self.add_argument('-s', '--esa-password', help = 'ESA SSH password', default = '')
        self.add_argument('-p', '--esa-ssh-port', help = 'ESA SSH port', default = 22)

    def __add_email_arguments(self):
        """Method to register the CLI email arguments"""
        self.add_argument('--send-mail', dest = 'send_mail', action = 'store_true')
        self.set_defaults(send_mail = False)
        self.add_argument('-o', '--case-owner', help = 'Case owner email', default = '')
        self.add_argument('-n', '--case-number', help = 'Case ID number', default = '')


class LoggerInitializer:
    """Class to get the Logging parameters and initialize the logger"""

    @staticmethod
    def initialize():
        """Initializes the logger with the provided CLI arguments."""
        arguments = ESACLIArguments().arguments
        # We clear the logfile
        LoggerInitializer.__delete_log_file()
        # We set the logfile name via the received parameter
        Logger.output_log_file_name = arguments.logfile_name

        # We initialize the logger instance
        Logger.initialize(
            verbose = arguments.verbose
        )

    @staticmethod
    def __delete_log_file():
        """Deletes the log file"""
        FileManager(Logger.output_log_file_name).delete_file()
        

class ESASSHParametersGetter:
    """Class to get the SSH parameters and create the ESASSHParameters container."""
    def __init__(self):
        self.esa_ssh_parameters: ESASSHParameters = None
        self.set()

    def set(self):
        """Retrieves the SSH parameters from CLI arguments."""
        args = ESACLIArguments().arguments
        self.esa_ssh_parameters = ESASSHParameters(args.esa_ip, args.esa_user, args.esa_password, args.esa_ssh_port)

    def get(self) -> ESASSHParameters:
        """Returns the SSH parameters instance"""
        return self.esa_ssh_parameters


class ESAEmailParametersGetter:
    """Class to get the Email parameters and create the ESAEmailParameters container."""
    def __init__(self):
        self.esa_email_parameters: ESAEmailParameters = None
        self.set()

    def set(self):
        """Retrieves the Email parameters from CLI arguments."""
        args = ESACLIArguments().arguments
        self.esa_email_parameters = ESAEmailParameters(args.send_mail, args.case_owner, args.case_number)

    def get(self) -> ESAEmailParameters:
        """Returns the Email parameters instance"""
        return self.esa_email_parameters

# Facade
class ESAParameters:
    """
    @version 3.0.0

    Facade to access to the parameters for SSH and email retrieved from the CLI arguments.
    """
    def __init__(self):
        # We initialize the logger
        LoggerInitializer.initialize()
        # We set the SSH and email parameters
        self.esa_ssh_parameters: ESASSHParameters = ESASSHParametersGetter().get()
        self.esa_email_parameters: ESAEmailParameters = ESAEmailParametersGetter().get()

        