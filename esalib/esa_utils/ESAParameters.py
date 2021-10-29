import click
from dataclasses import dataclass
# Utils
from utils.logger.Logger import Logger


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

    @click.command()
    @click.option(
        '--verbose', 
        is_flag = True, 
        metavar = '<Flag to show all messages>',
        help = 'Sets the log level to INFO, to display all the messages'
    )
    @click.option(
        '-v', '--verbose-level',
        count = True,
        default = 3,
        metavar = '<-v * n times>',
        help = (
            'Sets the log level according to the repetitions of the letter "v" as follows:\n\n' 
            '   - 1 time (-v): DEBUG level (all messages are logged)\n\n'
            '   - 2 times (-vv): INFO level (all messages, except from debug ones, are displayed)\n\n'
            '   - 3 times (-vvv): WARNING level (only warnings and errors are logged)\n\n'
            '   - 4 times (-vvvv): ERROR level (only errors and critical exceptions are logged)\n\n'
            '   - 5 times (-vvvvv): CRITICAL level (only critical errors are logged)\n\n'
        )
    )
    @click.option(
        '--logfile-name',
        default = 'app.log',
        metavar = '<Output logfile name>',
        show_default = True,
        help = 'The name of the output logfile'
    )
    def initialize(
        self,
        verbose,
        verbose_level,
        logfile_name
    ):
        """Initializes the logger with the provided CLI arguments."""
        # We set the logfile name via the received parameter
        Logger.output_log_file_name = logfile_name

        # We determine the verbose_level
        logger_level = Logger.get_normalized_logger_level(verbose_level)

        # We initialize the logger instance
        Logger.initialize(
            level = logger_level,
            verbose = verbose
        )
        

class ESASSHParametersGetter:
    """Class to get the SSH parameters and create the ESASSHParameters container."""
    def __init__(self):
        self.esa_ssh_parameters: ESASSHParameters = None
        # We set the parameters from CLI
        self.set()

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
        # We set the parameters from CLI
        self.set()

    @click.command()
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
    @version 0.1.0

    Facade to access to the parameters for SSH and email retrieved from the CLI arguments.
    """
    def __init__(self):
        # We initialize the logger
        LoggerInitializer().initialize()
        # We set the SSH and email parameters
        self.esa_ssh_parameters: ESASSHParameters = ESASSHParametersGetter().get()
        self.esa_email_parameters: ESAEmailParameters = ESAEmailParametersGetter().get()







        

