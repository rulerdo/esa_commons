import re
from typing import NewType
# ESA utils
from ..ESASSHAgent import ESASSHAgent
# Utils
from ...utils.logger.Logger import Logger

class BaseConfig:
    """
    @version 1.2.0

    Base class of the configuration options, it implements the base methods and business logic.
    """
    # Constants
    # The default configuration mode delimiter of CLI commands
    CONFIG_MODE_DELIMITER = ']>'
    # Configuration default values regex
    DEFAULT_CONFIG_VALUE_REGEX = re.compile(r'\[(.+)\]>')

    def __init__(
        self, 
        esa_ssh_agent: ESASSHAgent,
        config_mode_name: str = '',
        is_in_cluster_mode: bool = True
    ):
        """
        @param {ESASSHAgent} esa_ssh_agent Instance of the SSH agent, to request the execution of CLI commands.
        @param {str} config_mode_name The specific configuration that we want to enter (like destconfig, sshconfig, etc).
        """
        self.esa_ssh_agent: ESASSHAgent = esa_ssh_agent
        self.config_mode_name: str = config_mode_name
        self.is_in_cluster_mode: bool = is_in_cluster_mode
        # Internal state
        self.is_in_config_mode: bool = False
        self.config_nested_level: int = 1

    def set_config_mode_name(self, config_mode_name: str) -> None:
        """
        @param {str} config_mode_name The specific configuration that we want to enter (like destconfig, sshconfig, etc).
        """
        self.config_mode_name = config_mode_name
    
    def enter_config_mode(self) -> None:
        """
        Enters to configuration mode of the specific mode provided as argument.
        """
        self.esa_ssh_agent.execute_cli_command(self.config_mode_name, command_delimiter = self.CONFIG_MODE_DELIMITER)
        # We update the flag that indicates if we are in config mode
        self.is_in_config_mode = True
        Logger.info(f'Switched to { self.config_mode_name } mode.')

    def exit_config_mode(self) -> None:
        """Facade method to exit configuration mode by hitting ENTER."""
        # We get the escape sequence according to the nested level value, this indicates the required number of \n chars to exi configuration mode
        exit_sequence = ''.join('\n' for _ in range(self.config_nested_level))
        self.esa_ssh_agent.execute_cli_command(exit_sequence, command_delimiter = '(SERVICE)>')
        # We update the flag that indicates if we are in config mode
        self.is_in_config_mode = False
        Logger.info(f'Exiting { self.config_mode_name } mode.')

    def introduce_configuration_value(self, value: str) -> str:
        """
        @param {str} value Value to introduce to the configuration prompt.

        Facade method to introduce a specific configuration value.
        """
        output = self.esa_ssh_agent.execute_cli_command(value, command_delimiter = ']>')
        # We handle the case where the device asks for the configuration mode (cluster or individual machine) according to the value of is_in_cluster_mode
        return self.__enter_cluster_mode_option_if_requested(output, original_value = value)

    def increase_nested_config_level(self):
        """Method to increase by one the nested config level (it will indicate the number of \n to enter to exit configuration mode)."""
        self.config_nested_level += 1
    
    def leave_default_configuration_value(self) -> str:
        """Facade method to leave a default value by hitting ENTER (which is made after each command by ssh_agent)."""
        return self.esa_ssh_agent.execute_cli_command('', command_delimiter = ']>')

    def leave_all_default_configuration_values(self, log_outputs: bool = False) -> str:
        """Method to leave all the configuration """
        is_config_value_array_empty = False
        while not is_config_value_array_empty:
            output = self.leave_default_configuration_value()
            # We log the output if specified
            if log_outputs: 
                Logger.info(output)
            is_config_value_array_empty = self.__is_default_config_value_empty(output)
        Logger.info('All default values for requested configuration parameters were left.')

    # Internal methods
    def __enter_cluster_mode_option_if_requested(self, command_output: str, original_value: str) -> str:
        """
        @param {str} command_output The output of the executed command, which may contain the cluster warning.
        @param {str} original_value The value that was introduced before the configuration mode selection.

        Introduces the clustering option (1 or 2) if requested and resumes the originally requested option.
        """
        if not self.__is_cluster_warning_present(command_output):
            return command_output
        # We select the cluster configuration mode (1 for cluster 2 for individual machine)
        configuration_mode = '1' if self.is_in_cluster_mode else '2'
        self.introduce_configuration_value(configuration_mode)
        Logger.info(f'Option { configuration_mode } entered to warning [NOTICE: This configuration command has not yet been configured for the current cluster mode]')
        # We enter the original command and return the output
        return self.introduce_configuration_value(original_value)

    def __is_cluster_warning_present(self, command_output: str) -> bool:
        """
        @param {str} command_output The output of the executed command, which may contain the cluster warning.
        """
        return command_output.find('NOTICE: This configuration command has not yet been configured') != -1

    def __is_default_config_value_empty(self, command_output: str) -> bool:
        """
        @param {str} command_output The output of the executed command, which may contain default configuration values inside [].
        """
        return len(self.DEFAULT_CONFIG_VALUE_REGEX.findall(command_output)) == 0

class BaseConfigOperations:
    """Common configuration operations along various modes."""
    NEW         = 'NEW'
    EDIT        = 'EDIT'
    SETUP       = 'SETUP'
    DELETE      = 'DELETE'