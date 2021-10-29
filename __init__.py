import click
# Use case
from use_case.HighCPUUsageFix import HighCPUUsageFix
# Utils
from utils.logger.Logger import Logger


# CLI options

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
def main(
    verbose, 
    verbose_level, 
    logfile_name,
    # ESA parameters
    esa_ip,
    esa_user,
    esa_password,
    send_mail,
    case_owner,
    case_number
):
    initialize_logger(verbose, verbose_level, logfile_name)

    HighCPUUsageFix(
        esa_ip,
        esa_user,
        esa_password,
        send_case_email = send_mail,
        case_owner_email = case_owner,
        case_identification_number = case_number
    ).solve()



def initialize_logger(verbose, verbose_level, logfile_name):
    """
    Function to initialize the Logger instance with the parameters obtained from CLI options.
    Options for verbosity, logger-level and output lof file name are supported.
    """
    # We set the logfile name via the received parameter
    Logger.output_log_file_name = logfile_name

    # We determine the verbose_level
    logger_level = Logger.get_normalized_logger_level(verbose_level)

    # We initialize the logger instance
    Logger.initialize(
        level = logger_level,
        verbose = verbose
    )


if __name__ == '__main__':
    main()


