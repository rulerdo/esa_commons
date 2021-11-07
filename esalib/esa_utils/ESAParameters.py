import click
from dataclasses import dataclass
# Utils
from ..utils.logger.Logger import Logger


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


class LoggerInitializer:
    """Class to get the Logging parameters and initialize the logger"""

    def initialize(
        self,
        verbose,
        logfile_name
    ):
        """Initializes the logger with the provided CLI arguments."""
        # We set the logfile name via the received parameter
        Logger.output_log_file_name = logfile_name

        # We initialize the logger instance
        Logger.initialize(
            verbose = verbose
        )
        

class ESASSHParametersGetter:
    """Class to get the SSH parameters and create the ESASSHParameters container."""
    def __init__(self):
        self.esa_ssh_parameters: ESASSHParameters = None

    def set(
        self,
        esa_ip,
        esa_user,
        esa_password,
        esa_ssh_port
    ):
        """Retrieves the SSH parameters from CLI arguments."""
        self.esa_ssh_parameters = ESASSHParameters(esa_ip, esa_user, esa_password, esa_ssh_port)

    def get(self) -> ESASSHParameters:
        """Returns the SSH parameters instance"""
        return self.esa_ssh_parameters


class ESAEmailParametersGetter:
    """Class to get the Email parameters and create the ESAEmailParameters container."""
    def __init__(self):
        self.esa_email_parameters: ESAEmailParameters = None

    def set(
        self,
        send_mail,
        case_owner,
        case_number
    ):
        """Retrieves the Email parameters from CLI arguments."""
        self.esa_email_parameters = ESAEmailParameters(send_mail, case_owner, case_number)

    def get(self) -> ESAEmailParameters:
        """Returns the Email parameters instance"""
        return self.esa_email_parameters

# Facade
class ESAParameters:
    """
    @version 2.1.0

    Facade to access to the parameters for SSH and email retrieved from the CLI arguments.
    """
    @click.command()
    @click.option(
        '--esa-ip',
        default = '0.0.0.0',
        metavar = '<ESA IP>',
        help = 'ESA IP'
    )
    @click.option(
        '--esa-user',
        default = '0.0.0.0',
        metavar = '<ESA SSH user>',
        help = 'ESA SSH user'
    )
    @click.option(
        '--esa-password',
        default = '0.0.0.0',
        metavar = '<ESA SSH password>',
        help = 'ESA SSH password'
    )
    @click.option(
        '--esa-ssh-port',
        default = 22,
        metavar = '<ESA SSH port>',
        help = 'ESA SSH port'
    )
    @click.option(
        '--send-mail', 
        is_flag = True, 
        metavar = '<Flag to send the results by mail>',
        help = 'Indicates to send a mail to the case owner at the end of the remediation'
    )
    @click.option(
        '--case-number',
        default = 'NA',
        metavar = '<Case SR number>',
        help = 'Case identification number'
    )
    @click.option(
        '--case-owner',
        default = None,
        metavar = '<Case owner email>',
        help = 'Email of the TAC member assigned to this case'
    )
    @click.option(
        '--verbose', 
        is_flag = True, 
        metavar = '<Flag to show all messages>',
        help = 'Sets the log level to INFO, to display all the messages'
    )
    @click.option(
        '--logfile-name',
        default = 'app.log',
        metavar = '<Output logfile name>',
        show_default = True,
        help = 'The name of the output logfile'
    )
    def __init__(
        self,
        esa_ip,
        esa_user,
        esa_password,
        esa_ssh_port,
        # Email arguments
        send_mail,
        case_owner,
        case_number,
        # Logging arguments
        verbose, 
        logfile_name,

    ):
        # We initialize the logger
        LoggerInitializer().initialize(verbose, logfile_name)
        # We set the SSH parameters
        esa_ssh_parameters_getter =  ESASSHParametersGetter()
        esa_ssh_parameters_getter.set(esa_ip, esa_user, esa_password, esa_ssh_port)
        self.esa_ssh_parameters: ESASSHParameters = esa_ssh_parameters_getter.get()
        # We set the email parameters
        esa_email_parameters_getter = ESAEmailParametersGetter()
        esa_email_parameters_getter.set(send_mail, case_owner, case_number)
        self.esa_email_parameters: ESAEmailParameters = esa_email_parameters_getter.get()