import re
from collections import namedtuple
# ESA utils
from ..ESASSHAgent import ESASSHAgent
# Utils
from ...utils.logger.Logger import Logger

class DestconfigManager:

    def __init__(
        self,
        esa_ssh_agent: ESASSHAgent,
        is_in_cluster_mode: bool = True
    ):
        self.esa_ssh_agent = esa_ssh_agent
        self.is_in_cluster_mode = is_in_cluster_mode
        # Internal state
        self.list_entries = ''
        # We initialize the destconfig mode
        self.__initialize()

    def __initialize(self) -> None:
        configuration_mode = '1' if self.is_in_cluster_mode else '2'
        self.esa_ssh_agent.execute_cli_command('destconfig', command_delimiter = ']>')
        self.esa_ssh_agent.execute_cli_command(configuration_mode, command_delimiter = ']>')
        Logger.info('Switched to destconfig mode.')

    def list_configured_entries(self) -> str:
        self.list_entries = self.apply_operation_to_configured_entries('LIST')

    def find_configured_entry_by_domain(self, domain: str):
        regex = re.compile(f'{domain}\s*(\w+)\s*(\w+)\s*(\w+)\s*(\w+)\s*(\w+)\s*(\w+)')
        matches = regex.findall(self.list_entries)
        return matches.pop(0) if len(matches) > 0 else None

    def is_parameter_enabled_for_entry(self, parameter: str, configured_entry: tuple) -> bool:
        """
        """
        destconfig_parameters = DestconfigParameters(entry = configured_entry)
        return destconfig_parameters.is_parameter_enabled(parameter)

    def apply_operation_to_configured_entries(self, operation: str) -> str:
        """
        @param {str} operation Operation to apply.

        Facade method to introduce an operation to perform at configured entries level. Available operations are LIST, NEW, EDIT, DELETE, etc.
        """
        return self.esa_ssh_agent.execute_cli_command(operation, command_delimiter = ']>')

    def introduce_configuration_value(self, value: str) -> str:
        """
        @param {str} value Value to introduce to the configuration prompt.

        Facade method to introduce a specific configuration value. It does the same as the previous method, but it's more declarative and 
        avoids confusion.
        """
        return self.esa_ssh_agent.execute_cli_command(value, command_delimiter = ']>')

    def leave_default_configuration_value(self) -> str:
        """Facade method to leave a default value by hitting ENTER (which is made after each command by ssh_agent)."""
        return self.esa_ssh_agent.execute_cli_command('', command_delimiter = ']>')

    def exit_destconfig_mode(self) -> None:
        """Facade method to exit destconfig mode by hitting ENTER."""
        self.esa_ssh_agent.execute_cli_command('\n', command_delimiter = '(SERVICE)>')

# Parameters

"""
EntryParameters named tuple, to get the values in positional order.
It defined the shape of the output of destconfig (RateLimiting, TLS, Dane, BounceVerification, BounceProfile, IPVersion)
"""
EntryParameters = namedtuple(
    'EntryParameters', 'RateLimiting TLS Dane BounceVerification BounceProfile IPVersion'
)

class DestconfigParameters:
    """Class to manipulate the parameters and get normalized and predictable values and conditions from them."""

    def __init__(self, entry: EntryParameters):
        """
        @param {EntryParameters} The named tuple containing the values for the entry.
        """
        self.entry = entry

    def get_parameter(self, parameter: str):
        """
        @param {str} parameter Parameter to get.

        Returns the specified parameter from the named tuple.
        """
        return getattr(self.entry, parameter)

    def is_parameter_enabled(self, parameter: str) -> bool: 
        """
        @param {str} parameter Parameter to validate.

        Validates if the parameter is enabled (On).
        """
        return self.get_parameter(parameter) == 'On'

        
