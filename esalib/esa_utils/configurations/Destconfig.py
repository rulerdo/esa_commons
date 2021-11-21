import re
from collections import namedtuple
# Base configuration
from .BaseConfig import BaseConfig
# ESA utils
from ..ESASSHAgent import ESASSHAgent

class DestconfigManager(BaseConfig):
    """
    @version 2.0.0

    Class that provides methods to access and configure parameters in destconfig mode. It extends the base class BaseConfig to add 
    methods specific to destconfig mode, like cluster option and operations over domain entries.
    """

    def __init__(
        self,
        esa_ssh_agent: ESASSHAgent,
        is_in_cluster_mode: bool = True
    ):
        # We initialize the parent class
        super().__init__(
            esa_ssh_agent = esa_ssh_agent, 
            config_mode_name = 'destconfig',
            is_in_cluster_mode = is_in_cluster_mode
        )
        # Internal state
        self.list_entries = ''
        # We initialize the destconfig mode
        self.__initialize()

    def __initialize(self) -> None:
        """Enters to configuration mode (destconfig) and introduces the clustering option (1 or 2)."""
        configuration_mode = '1' if self.is_in_cluster_mode else '2'
        # We enter to config mode (destconfig) and enter the option for cluster or individual settings
        self.enter_config_mode()
        self.esa_ssh_agent.execute_cli_command(configuration_mode, command_delimiter = ']>')
        

    def list_configured_entries(self) -> None:
        """Executes the list command and stores the output in an internal variable."""
        self.list_entries = self.apply_operation_to_configured_entries('LIST')

    def find_configured_entry_by_domain(self, domain: str):
        """
        @param {str} domain The domain whose configuration values we are going to search in the entries list.

        Finds all the configured values for a domain entry.
        """
        regex = re.compile(f'{domain}\s*(\w+)\s*(\w+)\s*(\w+)\s*(\w+)\s*(\w+)\s*(\w+)')
        matches = regex.findall(self.list_entries)
        return matches.pop(0) if len(matches) > 0 else None

    def is_parameter_enabled_for_entry(
        self, 
        parameter: str, 
        configured_entry: tuple
    ) -> bool:
        """
        @param {str} parameter The parameter to retrieve.
        @param {tuple} configured_entry The tuple that contains the configurations values for an specific entry.

        Mehtod to get the value of a parameter or specific configuration in the tuple containing the configured values for the entry.
        """
        destconfig_parameters = DestconfigParameters(entry = configured_entry)
        return destconfig_parameters.is_parameter_enabled(parameter)

    def apply_operation_to_configured_entries(self, operation: str) -> str:
        """
        @param {str} operation Operation to apply.

        Facade method to introduce an operation to perform at configured entries level. Available operations are LIST, NEW, EDIT, DELETE, etc.
        """
        return self.esa_ssh_agent.execute_cli_command(operation, command_delimiter = ']>')

    def exit_destconfig_mode(self) -> None:
        """Exits destconfig mode."""
        self.exit_config_mode()

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

        
